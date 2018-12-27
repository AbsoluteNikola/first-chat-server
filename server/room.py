import ujson
from collections import namedtuple

from sanic.websocket import WebSocketCommonProtocol
from websockets.exceptions import ConnectionClosed


_User = namedtuple('User', ['name', 'ws'])


class Room:
    def __init__(self, name):
        self._name = name
        self._clients = []

    def add_user(self, name: str, ws: WebSocketCommonProtocol):
        print(f'new user {name}')
        self._clients.append(_User(name, ws))

    async def send_message(self, **kwargs):
        for i, user in enumerate(self._clients):

            if user.name == kwargs.get('name'):
                continue

            try:
                await user.ws.send(ujson.dumps(kwargs))
            except ConnectionClosed:
                del self._clients[i]

    def __len__(self):
        return len(self._clients)
