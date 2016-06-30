from addon import hookup
from addon.runner import Runner
from addon.hookup import ApiConnector
from addon.message_handler import MessageHandler, PrettyMessagePrint

if __name__ == '__main__':

    runner = Runner(ApiConnector(), [PrettyMessagePrint()])
    runner.join()