from core.message_handler import *

class PrettyMessagePrint(UserMessageHandler):

    def __init__(self, params):
        pass

    def handle_user_message(self, message):
        sender = message.sender
        if sender is not None:
            printable = sender + " sent a message "
            if message.has_text():
                printable = sender + ": " + message.text
            print(printable)