import json

from slacker import Slacker

from .exception import ConnectorException
from .ws import ws


class rtm:
    def __init__(self, token, callback=None):
        self.__token = token

        self.callback = callback

        self.__api = Slacker(token)
        self.__ws = ws(token, self.callback)

        self.__message_id = 1

    @property
    def api(self):
        return self.__api

    @property
    def callback(self):
        return self.__callback

    @callback.setter
    def callback(self, func):
        def loader(message):
            func(json.loads(message))
        self.__callback = loader

    @property
    def is_connected(self):
        return self.__ws.is_connected

    def connect(self, background=False):
        if self.is_connected:
            return
        self.__ws.callback = self.callback
        self.__ws.connect(background=background)

    def disconnect(self):
        if not self.is_connected:
            return
        self.__ws.disconnect()

    def send(self, message, channel, type='message'):
        if not self.is_connected:
            raise RtmException('not connect slack websocket')

        id = self.__message_id
        self.__message_id += 1
        default_message = {
            'id': id,
            'type': type,
            'channel': channel,
            'text': message
        }
        self.__ws.send(json.dumps(default_message))
        return id

