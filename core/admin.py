from core.message_handler import MessageHandler

class AdminHandler(MessageHandler):

    def __init__(self, api_connection, handler_list, admin_bot):
        self.handler_list = handler_list
        self.api_connection = api_connection
        self.admin_bot = admin_bot

    def handle(self, message):
        pass
