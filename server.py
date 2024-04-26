import grpc
import chat_pb2
import chat_pb2_grpc
import redis
from concurrent import futures

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, name_server):
        self.name_server = name_server

    def Connect(self, request, context):
        ip_address, port = self.name_server.get_user_address(request.username)

        if ip_address and port:
            response = chat_pb2.ConnectionResponse(connected=True, ip_address=ip_address, port=port)
        else:
            response = chat_pb2.ConnectionResponse(connected=False)

        return response

    def SendMessage(self, request, context):
        recipient_ip, recipient_port = self.name_server.get_user_address(request.recipient_username)

        if recipient_ip and recipient_port:
            channel = grpc.insecure_channel(f"{recipient_ip}:{recipient_port}")
            stub = chat_pb2_grpc.ChatServiceStub(channel)

            message = chat_pb2.ChatMessage(sender_username=request.sender_username, message=request.message)
            stub.ReceiveMessage(message)

            return chat_pb2.Empty()
        else:
            context.set_details(f"El usuario '{request.recipient_username}' no está disponible.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return chat_pb2.Empty()

    def ReceiveMessage(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('ReceiveMessage method is not implemented on the server side.')
        raise NotImplementedError('ReceiveMessage method is not implemented on the server side.')

class NameServer:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

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

    name_server.register_user('Pepe', '192.168.1.100', 6000)
    name_server.register_user('Anna', '192.168.1.101', 6001)

    run_server()
