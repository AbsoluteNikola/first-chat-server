import websockets
import asyncio
import ujson

from random import choice
from string import ascii_letters
from time import sleep


def gen():
    return ''.join([choice(ascii_letters) for _ in range(10)])


async def main():
    name = 'A'
    async with websockets.connect(f'ws://localhost:8000/chat?name={name}&room=1') as ws:
        while True:
            msg = gen()
            await ws.send(ujson.dumps({
                'type': 'text',
                'name': name,
                'data': msg
            }))
            print(await ws.recv())
            sleep(5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())