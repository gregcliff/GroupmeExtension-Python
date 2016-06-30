from addon import hookup
from addon.runner import Runner
from addon.hookup import ApiConnector
from addon.bots import get_bot_by_name
from addon.message_handler import MessageHandler, PrettyMessagePrint, Echo

if __name__ == '__main__':

    runner = Runner(ApiConnector(), [MessageHandler(), PrettyMessagePrint(), Echo(get_bot_by_name("Johnny Five"))])
    runner.join()