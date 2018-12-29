import ujson
from collections import namedtuple

from sanic.websocket import WebSocketCommonProtocol
from websockets.exceptions import ConnectionClosed


class UserAlreadyExists(Exception):
    pass


class Room:
    def __init__(self, name):
        self._name = name
        self._clients = {}

    def add_user(self, name: str, ws: WebSocketCommonProtocol):
        if name in self._clients:
            raise UserAlreadyExists

        print(f'new user {name}')
        self._clients[name] = ws

    async def send_message(self, **kwargs):
        to_del = []
        for i, (name, ws) in enumerate(self._clients.items()):
            if name == kwargs.get('name'):
                continue

            try:
                await ws.send(ujson.dumps(kwargs))
            except ConnectionClosed:
                to_del.append(name)

        for name in to_del:
            self._clients.pop(name)

    def __len__(self):
        return len(self._clients)
