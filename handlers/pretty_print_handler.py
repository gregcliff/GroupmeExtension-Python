import core
from core.message_handler import *

class PrettyMessagePrint(MessageHandler):

    def __init__(self, params):
        pass

    def handle(self, message):
        for i in range(len(message)):
            if is_from_bot(message[i]): continue
            sender = get_sender(message[i])
            text = get_text(message[i])
            if sender is not None:
                printable = sender + " sent a message "
                if text is not None:
                    printable = sender + ": " + text
                print(printable)
