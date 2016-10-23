from core.runner import Runner
from core.hookup import ApiConnector
from core.util import get_handler_instances
from core.admin import AdminHandler

if __name__ == '__main__':
    connector = ApiConnector()
    handlers = get_handler_instances()
    admin_bot = None
    runner = Runner(connector, AdminHandler(connector, handlers, admin_bot), handlers)
    runner.join()