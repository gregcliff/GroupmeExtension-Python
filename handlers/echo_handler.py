from core.message_handler import *

class Echo(UserMessageHandler, BotMessageHandler):

    def __init__(self, params):
        UserMessageHandler.__init__(self)
        BotMessageHandler.__init__(self, params)

    def handle_user_message(self, message):
        if not message.is_from_bot() and message.has_text():
            self.bot.say(message.text)