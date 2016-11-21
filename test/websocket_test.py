from core.hookup import ApiConnector
from core.bots import get_bot_by_name
from core.message import Message
import unittest
from time import sleep, time
import logging

class TestWebsocketStayAlive(unittest.TestCase):

    def test_getting_messages(self):
        apiConnector = ApiConnector()
        last_initialization = time()
        apiConnector.initialize()
        bot = get_bot_by_name("Johnny Five")

        reinitialize_seconds = 60 * 15
        test_time_in_seconds = 60 * 30
        num_talkbacks = 10
        received_talkbacks = 0
        sleep_duration = test_time_in_seconds / num_talkbacks
        max_wait_in_seconds = 10
        start_time = time()
        last_message_sent = start_time
        waiting = False
        while received_talkbacks < num_talkbacks:
            current = time()
            if waiting:
                # check the messages to make sure we get it in the websocket
                messages = [Message(m).text for m in apiConnector.check_for_message()]
                if text in messages:
                    waiting = False
                    received_talkbacks += 1
                    logging.info("Received message " + str(text))
                else:
                    if current - last_message_sent > max_wait_in_seconds:
                        bot.say("Did not get message " + str(received_talkbacks) + " after " +
                                str(time() - start_time) + " .")
                        logging.error("Did not get message " + str(received_talkbacks) + ".")
                        assert False
            else:
                if current - last_message_sent > sleep_duration:
                    text = "Testing " + str(received_talkbacks)
                    bot.say(text)
                    last_message_sent = current
                    waiting = True

                if current - last_initialization > reinitialize_seconds:
                    apiConnector.initialize()
                    last_initialization = current
            sleep(.005)
        else:
            bot.say("Test successful.")
            logging.info("Successfully received all " + str(num_talkbacks) + " messages.")
