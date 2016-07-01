import addon.util

class Bot(object):

    def __init__(self, bot_id, group_id, name):
        self.bot_id = bot_id
        self.group_id = group_id
        self.name = name

    def say(self, text, picture=None):
        addon.util.publish_bot_message(self.bot_id, text, picture_url=picture)

def destroy_bot(bot):
    pass

def destroy_bot_by_id(bot_id):
    pass

def get_or_create_bot(name, group_id):
    pass

def create_bot(name, group_id):
    pass

def get_bot_by_name(name):
    bot_data = addon.util.get_bot_by_name(name)
    if bot_data is not None:
        bot = Bot(bot_data['bot_id'], bot_data['group_id'], bot_data['name'])
        return bot
    else:
        return None