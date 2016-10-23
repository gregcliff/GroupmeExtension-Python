from core.message_handler import TaggedMessageHandler, BotMessageHandler
from core.util import get_messages, get_config_info
from features.markov_chain import generate


class SpeechGeneratorHandler(TaggedMessageHandler, BotMessageHandler):

    def __init__(self, params):
        BotMessageHandler.__init__(self, params)
        TaggedMessageHandler.__init__(self, 'speak')
        self.number_sentences = 2 if 'sentences' not in params else params['sentences']
        self.order = 2 if 'order' not in params else params['order']
        self.number_of_messages = 100 if 'sample_size' not in params else params['order']
        self.group_key = 'real_group_id' if 'sample_source' not in params else params['sample_source']

    def handle_tagged_message(self, message):
        group_id = get_config_info()[self.group_key]
        gen = generate(
            get_messages(group_id, self.number_of_messages),
            self.number_sentences, self.order)
        self.bot.say(gen)