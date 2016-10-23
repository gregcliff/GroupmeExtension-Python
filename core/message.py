class Message(object):

    def __init__(self, raw_message):
        # bug with setting text 10/22
        self.raw_message = raw_message
        self.tags = get_tags(raw_message)
        self.sender_id = get_sender_id(raw_message)
        self.sender = get_sender(raw_message)
        self.sender_type = get_sender_type(raw_message)
        self.text = get_text(raw_message)

    def is_from_bot(self):
        return self.sender_type == 'bot'

    def has_text(self):
        return self.text is not None

    def __str__(self):
        return self.raw_message

def get_sender(message):
    return message['name']

def get_sender_id(message):
    return message['user_id']

def get_sender_type(message):
    return message['sender_type']

def get_text(message):
    return message['text']

def get_tags(message, tag_marker='#'):
    text = get_text(message)
    tags = []
    tag_state = False
    current_tag = ''
    if text is not None:
        for c in text:
            if c == tag_marker:
                tag_state = True
            elif c == ' ':
                tag_state = False
                if len(current_tag) > 0:
                    tags.append(current_tag)
                current_tag = ''
            elif tag_state:
                current_tag += c
        else:
            if tag_state and len(current_tag) > 0:
                tags.append(current_tag)

    return tags

def is_from_bot(message):
    return get_sender_type(message) == 'bot'