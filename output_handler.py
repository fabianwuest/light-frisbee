import asyncio
import dataclasses
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from typing import Union, List, Set, Tuple
import copy

import requests

import settings


class ThingSpeakManager:

    def __init__(self):
        self.elapsed_time = 0
        self.items_passed = 0
        self.min_message_interval = settings.RASPI_CONFIG.send_rate

        self.updates = []


async def thingspeak_out(queue_out: asyncio.Queue) -> None:
    start_time = time.time()
    items_passed = 0
    min_message_interval = settings.RASPI_CONFIG.send_rate
    cache = []

    while True:
        try:
            item = queue_out.get_nowait()
            cache.append(item)
        except asyncio.QueueEmpty:
            # print('No item available')
            await asyncio.sleep(0.05)

        elapsed_time = time.time() - start_time

        if elapsed_time >= min_message_interval and len(cache) > 0:
            # bulk write cache to thingspeak
            # print(f'Bulk write this to ThingSpeak: {len(cache)}')
            # print(f'Elapsed time: {elapsed_time}')
            fieldX_temp = {
                'field1': len(cache),
                'field2': cache,
            }
            fieldX = copy.deepcopy(fieldX_temp)
            cache.clear()
            await write_thingspeak(fieldX, datetime.now())

            start_time = time.time()
        elif elapsed_time >= min_message_interval and len(cache) == 0:
            start_time = time.time()

        await asyncio.sleep(0.05)




    """while True:

        while not queue_out.empty() and elapsed_time < min_message_interval:
            

            try:
                item = queue_out.get_nowait()
                cache.append(item)
                elapsed_time = time.time() - start_time
            except asyncio.QueueEmpty:
                # elapsed_time = time.time() -start_time
                pass

            # if elapsed_time >= min_message_interval:
                # send to thingspeak
                #nonlocal elapsed_time
                elapsed_time = 0 # reset timer
                start_time = time.time() # reset timer
                pass

            elapsed_time = time.time()


        else:
            pass

        await asyncio.sleep(0.05)"""

    """while True:

        obj = await queue_out.get()
        # print(f'from queue: {obj}')
        cache.append(obj)
        print(f'cache: {cache}')
        await asyncio.sleep(0.05)"""


async def write_thingspeak(fieldX: Dict[str, Any], created_at: datetime) -> dict:
    """ Send data to ThingSpeak.

    :param fieldX: (Optional) Field X data, where X is the field ID.
    :param created_at: (Optional) Timestamp of the data when it was created.
    :return: Returns the response to the POST request, which is a dict object of the new entry.
    """
    url_request = 'https://api.thingspeak.com/update.json'
    data = {
        'api_key': settings.THINGSPEAK_WRITE_API_KEY,
        'created_at': created_at if created_at is not None else ''
    }
    if fieldX is not None:
        data.update(fieldX)

    response = requests.post(url_request, data=data)
    return response.json()


@dataclass
class Update:
    created_at: datetime = None
    delta_t: int = None
    fieldX: Dict[str, Any] = None

    def __post_init__(self):
        self.created_at = self.created_at.isoformat() if self.created_at is not None else ''

    def to_dict(self) -> dict:
        as_dict = dataclasses.asdict(self)
        as_dict.__delitem__('fieldX')
        as_dict.__setitem__()
        as_dict.update(self.fieldX)  # fieldX could be None
        print(as_dict)

        """
        if self.fieldX is not None:
            dataclasses.asdict()"""
        return as_dict

    def alternative(self):
        re = {
            'created_at': self.created_at,
            'delta_t': self.delta_t,
        }
        if self.fieldX is not None:
            re.update(self.fieldX)
        return re


def bulk_write_json_data(updates: Union[List[Update], Set[Update], Tuple[Update]]) -> dict:
    url_request = f'https://api.thingspeak.com/channels/{settings.THINGSPEAK_CHANNEL_ID}/bulk_update.json'
    data = {
        'write_api_key': settings.THINGSPEAK_WRITE_API_KEY,
        'updates': [update.alternative() for update in updates]
    }
    # updates = [update.to_dict() for update in updates]
    # data.update({'updates': updates})
    print(data)

    # The response is a JSON object indicating success.
    response = requests.post(url_request, json=data)
    return response.json()


def cli_out():
    pass
