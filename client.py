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

        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.rabbitmq_exchange = None

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

    def setup_rabbitmq(self, chat_id):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_exchange = 'chat_id'
            self.rabbitmq_channel.exchange_declare(exchange=self.rabbitmq_exchange, exchange_type='fanout')
        except pika.exceptions.AMQPError as e:
            print (f"Error de RabbitMQ: {e}")


    def subscribe_to_group_chat(self, chat_id):
        self.setup_rabbitmq(chat_id)
        def message_listener():
            if self.rabbitmq_connection:
                #Declara cua temporal per subscriure't a l'exchange
                result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
                queue_name = result.method.queue
                self.rabbitmq_channel.queue_bind(exchange=self.rabbitmq_exchange, queue=queue_name)

                #Callback: Gestiona Missatges rebuts
                def callback(ch, method, properties, body):
                    message = body.decode('utf-8')
                    print(f"{chat_id}: {message}")

                #Consumeix missatges
                self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
                print(f"Subscrit a {chat_id}. Esperant missatges...")
                self.rabbitmq_channel.start_consuming()
            else:
                print("No s'ha establert conexió amb RabbitMQ.")

        thread=threading.Thread(target=message_listener)
        thread.start()

    def send_group_message(self, chat_id):
        if not self.rabbitmq_connection:
            print("No s'ha establer la conexió amb RabbitMQ")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Tancant conexió...")
                break
            message = f"{self.username}: {message}"
            self.rabbitmq_channel.basic_publish(exchange=self.rabbitmq_exchange, routing_key='', body=message.encode('utf-8'))

        self.rabbitmq_connection.close()

if __name__ == "__main__":
    username = input("Login: ")
    client = ChatClient(username)
    port_client = client.login()
    if port_client:
        while True:
            print("\n1. Connect To Chat")
            print("2. Subscribe to chat")
            print("3. Salir")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                chat_id = input("Chat al que vols connectar: ")
                client.connect_to_chat(chat_id)
                client.start_server(client, port_client)
            elif choice == "2":
                chat_id = input("Grup al que vols subscriure't : ")
                client.subscribe_to_group_chat(chat_id)
                client.send_group_message(chat_id)
            elif choice == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

