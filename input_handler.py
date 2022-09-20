import asyncio
import json
from datetime import datetime

import websockets
from websockets.exceptions import ConnectionClosed

import settings
from models import RecordingInstructions
from output_handler import write_thingspeak

import gpiozero

is_recording = False


# Send all possible Instructions in an enum on first connection?


# Instructions
async def frisbee_in(websocket: websockets.WebSocketClientProtocol) -> None:

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


def when_activated(sensor: gpiozero.input_devices.DigitalInputDevice) -> None:
    if not is_recording:
        return
    print('Object entered')


def when_deactivated(sensor: gpiozero.input_devices.DigitalInputDevice) -> None:
    if not is_recording:
        return
    print('Object left')


def wait_for_active_wrapper(sensor: gpiozero.input_devices.DigitalInputDevice) -> None:
    sensor.wait_for_active()


async def wait_for_inactive_wrapper(sensor: gpiozero.input_devices.DigitalInputDevice) -> None:
    sensor.wait_for_inactive()


async def sensor_recorder() -> None:

    # setup sensor
    sensor = gpiozero.DigitalInputDevice(settings.RASPI_CONFIG.gpio_pin, bounce_time=0.01)
    sensor.when_activated = when_activated
    sensor.when_deactivated = when_deactivated

    # coroutine needs to be running for the active and inactive events to be detected
    while True:
        await asyncio.sleep(0.05)  # yield control to event loop

    '''while True:

        while is_recording:
            
            await wait_for_active_wrapper(sensor)
            await wait_for_inactive_wrapper(sensor)
            
            """# coroutine needs to be running for the active and inactive events to be detected
            while True:
                await asyncio.sleep(0.05)  # yield control to event loop"""

            await asyncio.sleep(0.05)

        await asyncio.sleep(0.05)'''

    """while True:

        while is_recording:
            # read from sensor
            data = {'field1': 15}  # Sample

            if not settings.RASPI_CONFIG.no_output:
                print(data)

            if not settings.RASPI_CONFIG.test_mode:
                await write_thingspeak(data, datetime.now())  # TODO Blocking. Fix this.

            # await asyncio.sleep(settings.RASPI_CONFIG.sample_wait)
            await asyncio.sleep(0.05)

        await asyncio.sleep(0.05)"""
