import grpc
import chat_pb2
import chat_pb2_grpc
import redis
from concurrent import futures

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, name_server):
        self.name_server = name_server

    def Connect(self, request, context):
        username = request.username
        chat_id = request.chat_id


        ip_address, port = self.name_server.get_user_address(chat_id)

        if ip_address and port:
            return chat_pb2.ConnectionResponse(connected=True, ip_address=ip_address, port=port)
        else:
            return chat_pb2.ConnectionResponse(connected=False, ip_address="", port=0)
    def SendMessage(self, request, context):
        sender = request.sender
        recipient = request.recipient
        message = request.message

        ip_address, port = self.name_server.get_user_address(recipient)
        
        if ip_address and port:
            print(f"Mensaje enviado de {sender} a {recipient} en {ip_address}:{port}: {message}")
            return chat_pb2.MessageResponse(success=True)
        else:
            return chat_pb2.MessageResponse(success=False)


class NameServer:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

    def register_user(self, username, ip_address, port):
        user_info = f"{ip_address}:{port}"
        self.redis_client.set(username, user_info)


    def get_user_address(self, username):
        user_data = self.redis_client.get(username)
        if user_data:


            user_info = user_data.decode()
            ip_address, port_str = user_info.split(':')
            port = int(port_str)
            print(ip_address)
            print(port)
            return ip_address, port
        else:
            return None, None

    def close(self):
        self.redis_client.close()

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    name_server = NameServer()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(name_server), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    name_server = NameServer()

    name_server.register_user('Pepe', 'localhost', 6000)
    name_server.register_user('Anna', 'localhost', 6001)

    run_server()
