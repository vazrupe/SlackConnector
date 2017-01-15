import json
import time
import _thread

import websocket
from slacker import Slacker

from .exception import ConnectorException


class ws:
    def __init__(self, token, message_recv=None,
            on_open=None, on_close=None, on_error=None):
        self.__api = Slacker(token)
        self.__ws = None

        self.message_recv = message_recv

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error

    @property
    def is_connected(self):
        return self.__ws is not None

    def connect(self, background=False, url=None):
        if self.is_connected:
            return

        if not callable(self.message_recv):
            raise ConnectorException('functions that can not be executed')

        if url:
            connect_url = url
        else:
            res = self.__api.rtm.start()
            if res.successful:
                connect_url = res.body['url']
                time.sleep(1)
            else:
                raise res.error

        self.__ws = websocket.WebSocketApp(connect_url,
            on_message = ws.event(self.message_recv),
            on_error = self.on_error,
            on_close = self.on_close)
        self.__ws.on_open = self.on_open
        if background:
            _thread.start_new_thread(self.__ws.run_forever, ())
        else:
            self.__ws.run_forever()

    def disconnect(self):
        if not self.is_connected:
            return
        try:
            self.__ws.close()
        finally:
            self.__ws = None

    def send(self, message):
        if not self.is_connected:
            raise ConnectorException('not connect slack websocket')
        self.__ws.send(message)

    @staticmethod
    def event(func):
        '''
        Slack Websocket Wrapper
        '''
        def wrap(ws, *args, **kargs):
            func(*args, **kargs)
        return wrap
