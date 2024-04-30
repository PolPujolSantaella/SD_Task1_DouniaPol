import grpc
import chat_pb2
import chat_pb2_grpc
import redis
from concurrent import futures
import time
import pika

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.name_server = NameServer()
        self.message_broker = MessageBroker()

    def Login(self, request, context):
        username = request.username
        address = self.name_server.get_user_address(username)
        if address:
            print (f"Usuari {username} ha iniciat!")
            ip, port = address.split(':')
            return chat_pb2.Response(success=True, message="Usuari Registrat", ip=ip, port=int(port))
        else:
            return chat_pb2.Response(success=False, message="Usuari no registrat")

    def Connect(self, request, context):
        chat_id = request.chat_id
        chat_address = self.name_server.get_user_address(chat_id)
        if chat_address:
            ip, port = chat_address.split(':')
            return chat_pb2.Response(success=True, message="", ip=ip, port=int(port))
        else:
            return chat_pb2.Response(success=False)

class NameServer:
    def __init__(self):
        try:
            self.redis_client = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
            self.redis_client.set("usr:Pepe", "127.0.0.1:50052")
            self.redis_client.set("usr:Anna", "127.0.0.1:50053")
            self.redis_client.set("usr:Dounia", "127.0.0.1:50054")
            self.redis_client.set("usr:Pol", "127.0.0.1:50055")
        except Exception as e:
            print(e)

    def get_user_address(self, user):
        return self.redis_client.get(f"usr:{user}")


class MessageBroker:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='group_chat', exchange_type='fanout')

    def publish_message(self, message):
        self.channel.basic_publish(exchange='group_chat', routing_key='', body=message)



def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run_server()
