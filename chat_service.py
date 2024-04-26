class ChatService:

    def __init__(self):
        self.message_set = set()

    def Connect(self, username, chat_id):
        return None
    def SendMessage(self, sender_username, message):
        print('Missatge de' + sender_username + 'Rebut: ' + message)
        self.message_set.add(message)
        return 'Done'

    def ReceiveMessage(self):
        return list(self.message_set)

chat_service = ChatService()
