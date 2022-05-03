import ujson

from websockets.exceptions import ConnectionClosed


class UserAlreadyExists(Exception):
    pass


class Room:
    def __init__(self, name: str):
        self._name = name
        self._clients = {}

    def add_user(self, name: str, ws):
        if name in self._clients:
            raise UserAlreadyExists

        print(f'new user {name}')
        self._clients[name] = ws

    async def send_message(self, **kwargs):
        expired_user = []
        for i, (name, ws) in enumerate(self._clients.items()):
            try:
                await ws.send(ujson.dumps(kwargs))
            except ConnectionClosed:
                expired_user.append(name)

        for name in expired_user:
            del self._clients[name]

    def __len__(self):
        return len(self._clients)
