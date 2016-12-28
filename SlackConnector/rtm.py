import json

from slacker import Slacker

from .exception import ConnectorException
from .ws import ws


class rtm:
    def __init__(self, token, callback=None,
            on_open=None, on_close=None, on_error=None):
        self.__token = token

        self.message_recv = message_recv

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error

        self.__api = Slacker(token)
        self.__ws = ws(token, self.message_recv)

        self.__message_id = 1

    @property
    def api(self):
        return self.__api

    @property
    def message_recv(self):
        return self.__message_recv

    @callback.setter
    def message_recv(self, func):
        def loader(message):
            func(json.loads(message))
        self.__message_recv = loader

    @property
    def is_connected(self):
        return self.__ws.is_connected

    def connect(self, background=False):
        if self.is_connected:
            return
        self.__ws.on_open = self.on_open
        self.__ws.on_close = self.on_close
        self.__ws.on_error = self.on_error
        self.__ws.message_recv = self.message_recv
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

