import grpc
import chat_pb2
import chat_pb2_grpc
import pika
from concurrent import futures
import threading

class ChatClient(chat_pb2_grpc.ChatClientServicer):
    def __init__(self, username):
        self.username = username
        self.server_channel = grpc.insecure_channel('localhost:50051')
        self.server_stub = chat_pb2_grpc.ChatServiceStub(self.server_channel)

        self.user_channel = None
        self.user_stub = None

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def login (self):
        request = chat_pb2.LoginRequest(username=self.username)
        response = self.server_stub.Login(request)
        if response.success:
            print (f"{response.message}: {response.ip}:{response.port}")
            return response.port
        else:
            print (f"{response.message}")
            return None

    def connect_to_chat(self, chat_id):
        request = chat_pb2.ChatRequest(username=self.username, chat_id=chat_id)
        response = self.server_stub.Connect(request)
        if response.success:
            print(f"\t CHAT {chat_id}")
            self.user_channel = grpc.insecure_channel(f'{response.ip}:{response.port}')
            self.user_stub = chat_pb2_grpc.ChatClientStub(self.user_channel)
            return response.ip, response.port
        else:
            print(f"No s'ha pogut conectar amb {chat_id}")
            return None

    def send_messages(self, message, username):
        request = chat_pb2.Message(sender=self.username, message=message)
        response = self.user_stub.ReceiveMessage(request)
        if not response.success:
            print("El destinatari no està conectat al chat.")

    def ReceiveMessage(self, request, context):
        print (f"{request.sender}: {request.message}")
        return chat_pb2.MessageResponse(success=True)

    def start_server(self, client, port_client):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2_grpc.add_ChatClientServicer_to_server(client, server)
        server.add_insecure_port(f'[::]:{port_client}')
        server.start()
        try:
            print ("(Per sortir Ctrl+C).")
            while True:
                    message = input("")
                    client.send_messages(message, self.username)
        except KeyboardInterrupt:
            server.stop(0)



    def subscribe_to_group_chat(self, chat_id):
        #Estbalir conexió(__init__)
        #Declara cua temporal per subscriure't a l'exchange
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=chat_id, queue=queue_name)

        #Callback: Gestiona Missatges rebuts
        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"{chat_id}: {message}")

        #Consumeix missatges
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Subscrit a {chat_id}. Esperant missatges...")

        # Comença a consumir missatges
        self.channel.start_consuming()

    def send_group_message(self, chat_id, message):
        message = f"{self.username}: {message}"

        self.channel.basic_publish(exchange=chat_id, routing_key='',body=message.encode('utf-8'))
        print(f"{message}")


if __name__ == "__main__":
    username = input("Login: ")
    client = ChatClient(username)
    port_client = client.login()
    if port_client:
        while True:
            print("\n1. Connect To Chat")
            print("2. Subscribe to chat")
            print("3. Enviar Missatges Chat Grupal")
            print("4. Salir")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                chat_id = input("Chat al que vols connectar: ")
                client.connect_to_chat(chat_id)
                client.start_server(client, port_client)
            elif choice == "2":
                chat_id = input("Grup al que vols subscriure't : ")
                client.subscribe_to_group_chat(chat_id)
            elif choice == "3":
                chat_id = input("Grup al que vols enviar missatges : ")
                while True:
                    message = input("")
                    if message.lower() == "exit":
                        break
                    client.send_group_message(chat_id, message)
            elif choice == "4":
                break
            else:
                print("Opción inválida. Intente de nuevo.")
