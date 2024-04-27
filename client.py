import grpc
import chat_pb2
import chat_pb2_grpc

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

    def connect_to_chat(self, chat_id):
        request = chat_pb2.ConnectionRequest(username=self.username, chat_id=chat_id)
        response = self.stub.Connect(request)
        if response.connected:
            print(f"Conectat a {chat_id} en {response.ip_address}:{response.port}")
            return response.ip_address, response.port
        else:
            print(f"No s'ha pogut conectar a {chat_id}")
            return None, None


if __name__ == "__main__":
    username = input("Ingrese su nombre de usuario: ")
    client = ChatClient(username)

    while True:
        print("\n1. Connect To Chat")
        print("2. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            chat_id = input("Ingrese el nombre de usuario del destinatario: ")
            ip_address, port = client.connect_to_chat(chat_id)
        elif choice == "2":
            break
        else:
            print("Opción inválida. Intente de nuevo.")

