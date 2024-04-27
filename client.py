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
            print(f"Conectado a {chat_id} en {response.ip_address}:{response.port}")
            return response.ip_address, response.port
        else:
            print(f"No se pudo conectar a {chat_id}")
            return None, None

    def send_message(self, recipient, message):
        request = chat_pb2.MessageRequest(sender=self.username, recipient=recipient, message=message)
        response = self.stub.SendMessage(request)
        if response.success:
            print(f"Mensaje enviado a {recipient}")
        else:
            print(f"Error al enviar mensaje a {recipient}")
    

if __name__ == "__main__":
    username = input("Ingrese su nombre de usuario: ")
    client = ChatClient(username)

    while True:
        print("\n1. Conectar a chat")
        print("2. Enviar mensaje")
        print("3. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            chat_id = input("Ingrese el nombre de usuario del destinatario: ")
            ip_address, port = client.connect_to_chat(chat_id)
        elif choice == "2":
            recipient = input("Ingrese el nombre del destinatario: ")
            message = input("Ingrese el mensaje: ")
            client.send_message(recipient, message)
        elif choice == "3":
            break
        else:

            print("Opción inválida. Intente de nuevo.")
