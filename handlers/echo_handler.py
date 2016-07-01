import core
from core.message_handler import *

class Echo(MessageHandler):

    def __init__(self, params):
        self.bot = core.bots.get_or_create_bot(params['bot']['name'])

    def handle(self, message):
        for i in range(len(message)):
            text = get_text(message[i])
            if not is_from_bot(message[i]) and text is not None:
                self.bot.say(text)