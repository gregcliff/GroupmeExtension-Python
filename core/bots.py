import core.util
import logging

class Bot(object):

    def __init__(self, bot_id, group_id, name):
        self.bot_id = bot_id
        self.group_id = group_id
        self.name = name

    def say(self, text, picture=None):
        core.util.publish_bot_message(self.bot_id, text, picture_url=picture)

def destroy_bot(bot):
    pass

def get_or_create_bot(name, group_id=None):
    if group_id is None:
        group_id = core.util.get_config_info()['group_id']
    bots = core.util.get_bots()['response']
    bot_names = [b['name'] for b in bots]
    if name not in bot_names:
        bot_data = core.util.create_bot(name, group_id)
        logging.info("Created " + bot_data['name'])
    else:
        bot_data = [b for b in bots if b['name'] == name][0]
        logging.info("Got " + bot_data['name'])
    bot = Bot(bot_data['bot_id'], bot_data['group_id'], bot_data['name'])
    return bot

#"handlers.echo_handler.Echo":{"bot":{"name":"Johnny Five"}}

def get_bot_by_name(name):
    bot_data = core.util.get_bot_by_name(name)
    if bot_data is not None:
        bot = Bot(bot_data['bot_id'], bot_data['group_id'], bot_data['name'])
        return bot
    else:
        return None