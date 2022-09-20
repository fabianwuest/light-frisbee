import asyncio
import datetime
import json
import logging
from datetime import datetime

import websockets
from rich import print as rprint

import input_handler
import models
import settings


def start(args):
    settings.AUTH_CREDENTIALS = models.AuthCredentials(args.password,
                                                       args.label
                                                       )

    settings.RASPI_CONFIG = models.RaspiConfig(args.test_mode,
                                               args.sample_wait,
                                               args.send_rate,
                                               args.gpio_pin,
                                               args.mode,
                                               args.no_output
                                               )
    logging.basicConfig(level=logging.INFO)

    async def connect():
        # connect
        print(f'Attempting connection to {args.link} with participant label {args.label} ...')
        websocket = await websockets.connect(args.link)
        print(f'Connected successfully.')

        # authenticate
        print(f'Authenticating ...')
        await websocket.send(json.dumps(settings.AUTH_CREDENTIALS.asdict()))

        msg = await websocket.recv()

        if 'exception' in msg:
            # print(json.loads(msg)['exception'])
            rprint(f'{datetime.now().strftime(settings.TIME_FORMAT)} ' + '[bold]' + '[FRISBEE-Server]: ' + '[/bold]' +
                   '[red]' + json.loads(msg)['exception'] + '[/red]')
            return

        print(f'Authentication successful.')

        thingspeak_config = await websocket.recv()
        print(f'Received ThingSpeak Config: {thingspeak_config}')

        settings.THINGSPEAK_USER_API_KEY = json.loads(thingspeak_config)['config']['api_keys'][0]['api_key']

        # await asyncio.sleep(1)
        # print(websocket.close_code)
        # print(websocket.close_reason)

        await asyncio.gather(
            input_handler.frisbee_in(websocket),
            input_handler.sensor_recorder(),
        )

    asyncio.run(connect())
