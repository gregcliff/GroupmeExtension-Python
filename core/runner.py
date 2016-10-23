from core.hookup import ApiConnector
from core.message_handler import MessageHandler
from core.admin import AdminHandler
from core import util
import time
import logging
from core.message import Message

class Runner(object):
    run = True

    def __init__(self, api_connector : ApiConnector, admin_handler : AdminHandler, handlers : [MessageHandler]):
        self.connector = api_connector
        self.admin_handler = admin_handler
        print("Starting with:")
        for h in handlers:
            print("\t" + h.__class__.__name__)
        self.handlers = handlers

    def join(self):
        print("Connecting to Groupme pub sub service.")
        self.connector.initialize()
        while self.run:
            try:
                if int(time.time()) - self.connector.start > 60 * 10:
                    self.connector.initialize()
                messages = self.connector.check_for_message()
                for raw_message in messages:
                    message = Message(raw_message)
                    self.admin_handler.handle(message)
                    for handler in self.handlers:
                        try:
                            handler.handle(message)
                        except Exception as err:
                            logging.exception(err)
                            logging.info("Removing handler " + handler.__class__.__name__)
                            self.handlers.remove(handler)
            except Exception as exc:
                logging.exception(exc)
                logging.error("Error...but run forever.")
