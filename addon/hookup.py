from addon import util
from addon.message_handler import MessageHandler
import requests
import json
import time
import websocket

class ApiConnector(object):
    base_pub_sub_url = "https://push.groupme.com/faye"
    web_socket_url = "wss://push.groupme.com/faye"

    def get_id(self):
        self.id += 1
        return str(self.id)

    def __init__(self):
        self.start = int(time.time())
        self.id=0

    def initialize(self):
        p1 = self.p1()
        print("Sending " + str(p1))
        response = json.loads(requests.post(self.base_pub_sub_url, json=p1).text)
        print("Received " + str(response))
        self.client_id = response[0]['clientId']
        p2 = self.p2(self.client_id)
        print("Sending " + str(p2))
        response = json.loads(requests.post(self.base_pub_sub_url, json=p2).text)
        print("Received " + str(response))
        if bool(response[0]['successful']):
            self.socket = websocket.create_connection(self.web_socket_url)
            j = json.dumps(self.poll())
            print("Sending " + str(j))
            self.socket.send(j)
        else:
            print("Error connecting to websocket.")

    def p1(self):
        return [{
            "channel":"/meta/handshake",
            "version":"1.0",
            "supportedConnectionTypes":["long-polling", "websocket"],
            "id":self.get_id()
        }]

    def p2(self,client_id):
        return [
            {
                "channel": "/meta/subscribe",
                "clientId": client_id,
                "subscription": "/user/" + util.user_id(),
                "id": self.get_id(),
                "ext":
                    {
                        "access_token": util.get_key()
                    }
            }
        ]

    def poll(self):
        return [
            {
                "channel": "/meta/connect",
                "clientId": self.client_id,
                "connectionType": "websocket",
                "id": self.get_id()
            }
        ]

    def check_for_message(self):
        return json.loads(self.socket.recv())