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
        self.isConnected = {}

    def Login(self, request, context):
        username = request.username
        address = self.name_server.get_user_address(username)
        if address:
            print (f"Usuari {username} ha iniciat!")
            ip, port = address.split(':')
            self.isConnected[username] = False
            return chat_pb2.Response(success=True, message="Usuari Registrat", ip=ip, port=int(port))
        else:
            return chat_pb2.Response(success=False, message="Usuari no registrat")

    def Connect(self, request, context):
        chat_id = request.chat_id
        if self.isUserConnected(chat_id):
            return chat_pb2.Response(success=False, message="Usuari no Conectat o conectat amb algu altre")
        else:
            chat_address = self.name_server.get_user_address(chat_id)
            if chat_address:
                ip, port = chat_address.split(':')
                self.isConnected[chat_id] = True
                return chat_pb2.Response(success=True, message="Conexió establerta", ip=ip, port=int(port))
            else:
                return chat_pb2.Response(success=False, message="No s'ha trobat informació client")

    def isUserConnected(self, chat_id):
        return self.isConnected.get(chat_id, True)

    def UserUnconnected(self, request, context):
        username = request.username
        self.isConnected[username] = False
        response = chat_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

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

    def publish_message(self, chat_id, message):
        # Enviar el missatge al chat_id com a exchange.
        self.channel.basic_publish(exchange=chat_id, routing_key='',body=message)

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
