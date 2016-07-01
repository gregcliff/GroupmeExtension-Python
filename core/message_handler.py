import core.bots
import core.util

class MessageHandler(object):

    def __init__(self, params):
        pass

    def handle(self, message):
        print("Received message: " + str(message))

def get_sender(message):
    if 'data' in message and 'subject' in message['data']:
        if 'name' in message['data']['subject']:
            return message['data']['subject']['name']
    return None

def get_sender_id(message):
    if 'data' in message and 'subject' in message['data']:
        if 'user_id' in message['data']['subject']:
            return message['data']['subject']['user_id']
    return None

def get_sender_type(message):
    if 'data' in message and 'subject' in message['data']:
        if 'sender_type' in message['data']['subject']:
            return message['data']['subject']['sender_type']
    return None

def get_text(message):
    if 'data' in message and 'subject' in message['data']:
        if 'text' in message['data']['subject']:
            return message['data']['subject']['text']
    return None

def is_from_bot(message):
    return get_sender_type(message) == 'bot'