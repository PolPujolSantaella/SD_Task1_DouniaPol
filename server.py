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

class NameServer:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

    def register_user(self, username, ip_address, port):
        self.redis_client.hmset(username, {'ip_address': ip_address, 'port': port})

    def get_user_address(self, username):
        user_data = self.redis_client.hgetall(username)
        if user_data:
            return user_data.get(b'ip_address').decode(), int(user_data.get(b'port').decode())
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
