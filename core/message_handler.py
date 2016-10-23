from core.bots import *

class MessageHandler(object):

    def handle(self, message):
        print("Received message: " + str(message))

class UserMessageHandler(MessageHandler):

    def handle(self, message):
        if message.is_from_bot():
            return
        else:
            self.handle_user_message(message)

    def handle_user_message(self, message):
        pass

class TaggedMessageHandler(UserMessageHandler):

    def __init__(self, tag):
        self.tag = tag

    def handle_user_message(self, message):
        if self.tag in message.tags:
            self.handle_tagged_message(message)

    def handle_tagged_message(self, message):
        pass


class BotMessageHandler(MessageHandler):

    def __init__(self, params):
        self.bot = get_or_create_bot(params['bot']['name'])
