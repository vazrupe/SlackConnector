import json

from slacker import Slacker

from .exception import ConnectorException
from .ws import ws


class Rtm:
    def __init__(self, token, message_recv=None,
            on_open=None, on_close=None, on_error=None):
        self.__token = token

        self.__api = Slacker(token)
        self.__ws = ws(token)

        self.message_recv = message_recv

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error

        self.__message_id = 1
        self.__reply_callbacks = {}

    @property
    def api(self):
        return self.__api

    @property
    def is_connected(self):
        return self.__ws.is_connected

    def connect(self, background=False):
        if self.is_connected:
            return

        self.__ws.on_open = self.on_open
        self.__ws.on_close = self.on_close
        self.__ws.on_error = self.on_error

        def recv(message):
            msg = json.loads(message)
            reply_id = msg.get('reply_to')
            if reply_id is None:
                if self.message_recv is not None:
                    self.message_recv(msg)
            else:
                if reply_id in self.__reply_callbacks:
                    self.__reply_callbacks[reply_id](msg)
                    del self.__reply_callbacks[reply_id]
        self.__ws.message_recv = recv

        self.__ws.connect(background=background)

    def disconnect(self):
        if not self.is_connected:
            return
        self.__ws.disconnect()
        self.__reply_callbacks = {}

    def send(self, callback, type, **param):
        if not self.is_connected:
            raise RtmException('not connect slack websocket')

        id = self.__message_id
        self.__message_id += 1
        param['id'] = id
        param['type'] = type
        print(param)
        self.__ws.send(json.dumps(param))

        if callback is not None:
            self.__reply_callbacks[id] = callback
            
        return id

    def send_message(self, callback, channel, text):
        return self.send(callback, type='message', channel=channel, text=text)

    def typing_indicators(self, callback, channel):
        return self.send(callback, type='typing', channel=channel)

    def ping(self, callback):
        return self.send(callback, type='ping')
