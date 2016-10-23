from core.message_handler import BotMessageHandler, TaggedMessageHandler
from features.roast import generate_roast

class RoastHandler(BotMessageHandler, TaggedMessageHandler):

    def __init__(self, params):
        BotMessageHandler.__init__(self, params)
        TaggedMessageHandler.__init__(self, 'roast')

    def handle_tagged_message(self, message):
        self.bot.say("You " + generate_roast())