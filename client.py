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
        self.server = None

        self.user_channel = None
        self.user_stub = None
        self.connected = {}

        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.rabbitmq_exchange = None

        self.thread = None
        self.thread_stop = threading.Event()

    def login (self):
        request = chat_pb2.LoginRequest(username=self.username)
        try:
            response = self.server_stub.Login(request)
            if response.success:
                print (f"{response.message}: {response.ip}:{response.port}")
                return response.port
            else:
                print (f"{response.message}")
                return None
        except grpc.RpcError as e:
            print(f"Error de gRPC: {e}")
            return None

    def connect_to_chat(self, chat_id):
        request = chat_pb2.ChatRequest(username=self.username, chat_id=chat_id)
        try:
            response = self.server_stub.Connect(request)
            if response.success:
                self.connected[self.username] == chat_id
                print(f"\t CHAT {chat_id}")
                self.user_channel = grpc.insecure_channel(f'{response.ip}:{response.port}')
                self.user_stub = chat_pb2_grpc.ChatClientStub(self.user_channel)
            else:
                print(f"No s'ha pogut conectar amb {chat_id}")
        except grpc.RpcError as e:
            print(f"Error de gRPC: {e}")

    def send_messages(self, message, chat_id):
        if chat_id in self.connected and self.connected[chat_id] == self.username:
            request = chat_pb2.Message(sender=self.username, message=message)
            try:
                response = self.user_stub.ReceiveMessage(request)
                if not response.success:
                    print("El destinatari no està conectat al chat.")
            except grpc.RpcError as e:
                print(f"Error de gRPC: {e}")
        else:
            pass

    def ReceiveMessage(self, request, context):
        print (f"{request.sender}: {request.message}")
        return chat_pb2.MessageResponse(success=True)

    def start_server(self, client, port_client, chat_id):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2_grpc.add_ChatClientServicer_to_server(client, self.server)
        self.server.add_insecure_port(f'[::]:{port_client}')
        self.server.start()

        print ("(Per sortir escriu 'exit').")
        while True:
            message = input("")
            if message.lower() == "exit":
                break
            client.send_messages(message, chat_id)
        self.server.stop(0)

    def setup_rabbitmq(self, chat_id):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_exchange = 'chat_id'
            self.rabbitmq_channel.exchange_declare(exchange=self.rabbitmq_exchange, exchange_type='fanout')
        except pika.exceptions.AMQPError as e:
            print (f"Error de RabbitMQ: {e}")


    def subscribe_to_group_chat(self, chat_id):
        self.thread_stop.clear()
        self.setup_rabbitmq(chat_id)
        self.thread = threading.Thread(target=self.message_listener)
        self.thread.start()


    def message_listener(self):
        if self.rabbitmq_connection:
            #Declara cua temporal per subscriure't a l'exchange
            result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.rabbitmq_channel.queue_bind(exchange=self.rabbitmq_exchange, queue=queue_name)

            #Callback: Gestiona Missatges rebuts
            def callback(ch, method, properties, body):
                message = body.decode('utf-8')
                print(f"{message}")

            #Consumeix missatges
            self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print(f"Subscrit a {chat_id}. Esperant missatges...")
            while not self.thread_stop.is_set():
                self.rabbitmq_channel.connection.process_data_events()
        else:
            print("No s'ha establert conexió amb RabbitMQ.")

    def send_group_message(self, chat_id):
        if not self.rabbitmq_connection:
            print("No s'ha establer la conexió amb RabbitMQ")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Tancant conexió...")
                self.thread_stop.set()
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
                client.start_server(client, port_client, chat_id)
            elif choice == "2":
                chat_id = input("Grup al que vols subscriure't : ")
                client.subscribe_to_group_chat(chat_id)
                client.send_group_message(chat_id)
            elif choice == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")
