from core import util
from core.message_handler import MessageHandler
import requests
import json
import time
import websocket

class ApiConnector(object):
    base_pub_sub_url = "https://push.groupme.com/faye"
    web_socket_url = "wss://push.groupme.com/faye"
    TIMEOUT_SECONDS = 30

    def get_id(self):
        self.id += 1
        return str(self.id)

    def initialize(self):
        self.start = time.time()
        self.id = 0
        response = json.loads(requests.post(self.base_pub_sub_url, json=self.p1()).text)
        self.client_id = response[0]['clientId']
        response = json.loads(requests.post(self.base_pub_sub_url, json=self.p2(self.client_id)).text)
        if bool(response[0]['successful']):
            print("Successfully connected to push service.  Attempting to move to websocket.")
            self.socket = websocket.create_connection(self.web_socket_url)
            j = json.dumps(self.poll())
            self.socket.send(j)
            print("Success!")
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
        info = util.get_config_info()
        return [
            {
                "channel": "/meta/subscribe",
                "clientId": client_id,
                "subscription": "/user/" + info['user_id'],
                "id": self.get_id(),
                "ext":
                    {
                        "access_token": info['access_key']
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
        try:
            reinitialize_time = (self.start + self.TIMEOUT_SECONDS) - time.time()
            if reinitialize_time < 0:
                self.initialize()
                return []
            self.socket.settimeout(reinitialize_time)
            json_response = json.loads(self.socket.recv())
            return [unprocessed['data']['subject'] for unprocessed in json_response
                    if 'data' in unprocessed and 'subject' in unprocessed['data']]
        except websocket.WebSocketTimeoutException:
            self.initialize()
            return []