import asyncio
import json
from datetime import datetime

import websockets
from websockets.exceptions import ConnectionClosed

import settings
from models import RecordingInstructions
from output_handler import write_thingspeak

is_recording = False


# Send all possible Instructions in an enum on first connection?


# Instructions
async def frisbee_in(websocket: websockets.WebSocketClientProtocol) -> None:
    print('frisbee loop')
    try:
        async for message in websocket:
            print(message)

            if 'recording' in message:
                global is_recording

                match json.loads(message)['recording']:
                    case RecordingInstructions.START.value:
                        is_recording = True
                    case RecordingInstructions.PAUSE.value:
                        is_recording = False
                    case RecordingInstructions.STOP.value:
                        is_recording = False

            # await asyncio.sleep(0)

    except ConnectionClosed:
        # TODO: implement reconnect
        pass
    finally:
        # TODO: implement
        pass


async def sensor_recorder() -> None:

    while True:

        while is_recording:
            # read from sensor
            data = {'field1': 15}  # Sample

            if not settings.RASPI_CONFIG.no_output:
                print(data)

            if not settings.RASPI_CONFIG.test_mode:
                await write_thingspeak(data, datetime.now())  # TODO Blocking. Fix this.

            # await asyncio.sleep(settings.RASPI_CONFIG.sample_wait)
            await asyncio.sleep(0.05)

        await asyncio.sleep(0.05)
