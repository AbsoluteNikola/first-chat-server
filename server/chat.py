import ujson

from sanic import Sanic
from sanic import response
from sanic.request import Request
import sanic.exceptions as exs
from websockets.exceptions import ConnectionClosed
from room import Room, UserAlreadyExists
from loguru import logger


app = Sanic('chat')
app.static('/static', './static')
app.config.rooms = {}


@app.route('/')
async def index(_: Request):
    return await response.file('server/static/index.html')


async def chat_loop(name: str, room: Room, ws):
    while True:
        try:
            data = ujson.loads(await ws.recv())
            logger.info(f"New data in {name}'s chat loop. {data}")
        except ConnectionClosed:
            logger.info(f"Chat loop with {name} closed.")
            return
        await room.send_message(**data)


@app.websocket('/chat')
async def register_user(request: Request, ws):
    logger.info(f"Registering new user, paramsL {request.args}")
    if 'name' not in request.args or 'room' not in request.args:
        logger.warning("No args")
        exs.SanicException("Bad request", 400)

    name_arg = request.args['name'][0]
    room_arg = request.args['room'][0]

    if room_arg not in app.config.rooms:
        logger.info("Room not found. Creating new room.")
        app.config.rooms[room_arg] = Room(room_arg)

    room = app.config.rooms[room_arg]
    try:
        room.add_user(name_arg, ws)
    except UserAlreadyExists:
        logger.warning("User already exists, closing the socket")
        await ws.close(code=1003, reason='UserAlreadyExists')
    await chat_loop(name_arg, room, ws)
