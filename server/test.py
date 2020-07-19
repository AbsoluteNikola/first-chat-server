import websockets
import asyncio
import ujson

from random import choice
from string import ascii_letters


def random_str():
    return ''.join([choice(ascii_letters) for _ in range(10)])


async def echo_test():
    attempts = 5
    name = random_str()
    async with websockets.connect(f'ws://localhost:8000/chat?name={name}&room=1') as ws:
        for i in range(attempts):
            msg = random_str()
            data_to_echo = {
                'type': 'text',
                'name': name,
                'data': msg
            }
            await ws.send(ujson.dumps(data_to_echo))
            assert ujson.loads(await ws.recv()) == data_to_echo


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(echo_test())
