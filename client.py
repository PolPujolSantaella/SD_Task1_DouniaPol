import grpc
import chat_pb2
import chat_pb2_grpc
from concurrent import futures

class ChatClient(chat_pb2_grpc.ChatClientServicer):
    def __init__(self, username):
        self.username = username
        self.server_channel = grpc.insecure_channel('localhost:50051')
        self.server_stub = chat_pb2_grpc.ChatServiceStub(self.server_channel)

        self.user_channel = None
        self.user_stub = None

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
            print(f"Conectat al chat {chat_id} a {response.ip}:{response.port}")
            self.user_channel = grpc.insecure_channel(f'{response.ip}:{response.port}')
            self.user_stub = chat_pb2_grpc.ChatClientStub(self.user_channel)
            return response.ip, response.port
        else:
            print(f"No s'ha pogut conectar amb {chat_id}")
            return None

    def send_message(self, message):
        request = chat_pb2.Message(sender=self.username, message=message)
        response = self.user_stub.ReceiveMessage(request)

    def ReceiveMessage(self, request, context):
        print (f"{request.sender}: {request.message}")
        return chat_pb2.MessageResponse(success=True)

    def start_server(self, client, port_client):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chat_pb2_grpc.add_ChatClientServicer_to_server(client, server)
        server.add_insecure_port(f'[::]:{port_client}')
        server.start()
        try:
            while True:
                message = input("")
                client.send_message(message)
        except KeyboardInterrupt:
            server.stop(0)

if __name__ == "__main__":
    username = input("Ingrese su nombre de usuario: ")
    client = ChatClient(username)
    port_client = client.login()
    if port_client:
        while True:
            print("\n1. Connect To Chat")
            print("2. Salir")
            choice = input("Seleccione una opción: ")

            if choice == "1":
                chat_id = input("Ingrese el nombre de usuario del destinatario: ")
                client.connect_to_chat(chat_id)
                client.start_server(client, port_client)
            elif choice == "2":
                break
            else:
                print("Opción inválida. Intente de nuevo.")
