from datetime import datetime
from typing import Any, Dict

import requests

import settings


async def write_thingspeak(fieldX: Dict[str, Any], created_at: datetime) -> dict:
    """ Send data to ThingSpeak.

    :param fieldX: (Optional) Field X data, where X is the field ID.
    :param created_at: (Optional) Timestamp of the data when it was created.
    :return: Returns the response to the POST request, which is a dict object of the new entry.
    """
    url_request = 'https://api.thingspeak.com/update.json'
    data = {
        'api_key': settings.THINGSPEAK_USER_API_KEY,
        'created_at': created_at if created_at is not None else ''
    }
    if fieldX is not None:
        data.update(fieldX)

    response = requests.post(url_request, data=data)
    return response.json()


def cli_out():
    pass
