from addon.hookup import ApiConnector
from addon.message_handler import MessageHandler
from addon import util
import time

class Runner(object):
    run = True

    def __init__(self, connector : ApiConnector, handlers : [MessageHandler]):
        self.connector = connector
        self.handlers = handlers

    def join(self):
        print("Connecting to Groupme API.")
        self.connector.initialize()
        while self.run:
            if int(time.time()) - self.connector.start > 60 * 10:
                self.connector.initialize()
            message = self.connector.check_for_message()
            for handler in self.handlers:
                handler.handle(message)
