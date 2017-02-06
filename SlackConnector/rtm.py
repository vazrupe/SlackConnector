import json
import time
import _thread

from slacker import Slacker

from .exception import ConnectorException
from .ws import ws


class Rtm:
    def __init__(
            self,
            token,
            message_recv=None,
            on_open=None,
            on_close=None,
            on_error=None):
        self.__token = token

        self.__api = Slacker(token)
        self.__ws = ws(token)

        self.message_recv = message_recv

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error

        self.__message_id = 1
        self.__reply_callbacks = {}

        self.__last_ts = 0
        self.__reconnect_url = None

    @property
    def api(self):
        return self.__api

    @property
    def is_connected(self):
        return self.__ws.is_connected

    def run_forever(self, background=False, check_connect=30, ping_timeout=5):
        self.connect(background=True)

        def watch_dog():
            while True:
                time.sleep(check_connect)

                is_not_connected = not self.check_ping(ping_timeout)
                if is_not_connected:
                    self.reconnect()

        if background:
            _thread.start_new_thread(watch_dog, ())
        else:
            watch_dog()

    def check_ping(self, check_time=5):
        ok = [False]

        def pong(reply):
            type = reply.get('type')
            pong
            ok[0] = True
        self.ping(pong)
        time.sleep(check_time)

        return ok[0]

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
                    ts = float(msg['ts']) if 'ts' in msg else None
                    if ts is None or ts > self.__last_ts:
                        self.message_recv(msg)
                    self.__fetch_system(msg)
            else:
                if reply_id in self.__reply_callbacks:
                    self.__reply_callbacks[reply_id](msg)
                    del self.__reply_callbacks[reply_id]
        self.__ws.message_recv = recv

        self.__ws.connect(background=background)

    def __fetch_system(self, msg):
        ts = float(msg['ts']) if 'ts' in msg else None
        if ts and ts > self.__last_ts:
            self.__last_ts = ts

        type = msg.get('type')
        if type and type == 'reconnect_url':
            self.__reconnect_url = msg['url']

    def reconnect(self):
        if self.is_connected and self.__reconnect_url:
            self.__ws.disconnect()
            self.__ws.connect(background=False, url=self.__reconnect_url)

    def disconnect(self):
        if not self.is_connected:
            return
        self.__ws.disconnect()
        self.__reply_callbacks = {}
        self.__reconnect_url = None

    def send(self, type, callback=None, **param):
        if not self.is_connected:
            raise RtmException('not connect slack websocket')

        id = self.__message_id
        self.__message_id += 1
        param['id'] = id
        param['type'] = type

        self.__ws.send(json.dumps(param))

        if callback is not None:
            self.__reply_callbacks[id] = callback
        return id

    def send_message(self, channel, text, callback=None):
        return self.send(
            type='message',
            channel=channel,
            text=text,
            callback=callback
        )

    def typing_indicators(self, channel, callback=None):
        return self.send(type='typing', channel=channel, callback=callback)

    def ping(self, callback=None):
        return self.send(type='ping', callback=callback)
