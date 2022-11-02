import asyncio
import json
import logging
import time
from datetime import datetime

import websockets
from websockets.exceptions import ConnectionClosed

import output_handler
import settings
from models import DataPoint, RecordingInstructions
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


def when_activated(sensor: gpiozero.input_devices.DigitalInputDevice, datapoint: dict) -> None:
    if not is_recording:
        return
    datapoint['timestamp_enter'] = time.time()
    print(f'Object entered at {datapoint["timestamp_enter"]}')


def when_deactivated(sensor: gpiozero.input_devices.DigitalInputDevice,
                     datapoint: dict,
                     queue_out: asyncio.Queue) -> None:
    if not is_recording:
        return
    datapoint['timestamp_exit'] = time.time()
    queue_out.put_nowait(datapoint)
    print(f'Object exited at {datapoint["timestamp_exit"]}')


def wait_for_active_wrapper(sensor: gpiozero.input_devices.DigitalInputDevice, loop) -> None:
    # sensor.wait_for_active()
    print('waiting for active wrapper')
    loop.call_soon_threadsafe(sensor.wait_for_active)


def wait_for_inactive_wrapper(sensor: gpiozero.input_devices.DigitalInputDevice, loop) -> None:
    # sensor.wait_for_inactive()
    print('waiting for inactive wrapper')
    loop.call_soon_threadsafe(sensor.wait_for_inactive)


async def sensor_recorder(queue_out: asyncio.Queue) -> None:

    # setup sensor
    datapoint = dict(
        timestamp_enter=None,
        timestamp_exit=None,
    )
    sensor = gpiozero.DigitalInputDevice(settings.RASPI_CONFIG.gpio_pin, bounce_time=0.001)
    sensor.when_activated = lambda: when_activated(sensor, datapoint)
    sensor.when_deactivated = lambda: when_deactivated(sensor, datapoint, queue_out)

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
