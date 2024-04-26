import grpc
import chat_pb2
import chat_pb2_grpc

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

    def connect_to_chat(self, recipient_username):
        request = chat_pb2.ConnectionRequest(username=self.username)
        response = self.stub.Connect(request)

        if response.connected:
            ip_address = response.ip_address
            port = response.port
            print(f"Conectado al chat con {recipient_username}.")
            return ip_address, port
        else:
            print(f"No se pudo establecer conexión con {recipient_username}.")
            return None, None

    def send_message(self, recipient_username, message, ip_address, port):
        channel = grpc.insecure_channel(f"{ip_address}:{port}")
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        request = chat_pb2.SendMessageRequest(sender_username=self.username,
                                                   recipient_username=recipient_username,
                                                   message=message)
        response = stub.SendMessage(request)
        print("Mensaje enviado con éxito.")

    def receive_messages(self):
        # Este método no se implementa en el cliente
        pass

if __name__ == "__main__":
    username = input("Ingrese su nombre de usuario: ")
    client = ChatClient(username)

    while True:
        print("\n1. Enviar mensaje")
        print("2. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            recipient_username = input("Ingrese el nombre de usuario del destinatario: ")
            ip_address, port = client.connect_to_chat(recipient_username)
            message = input("Ingrese el mensaje a enviar: ")
            client.send_message(recipient_username, message, ip_address, port)
        elif choice == "2":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
