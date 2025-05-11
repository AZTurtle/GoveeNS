"""
Govee Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

import requests
from requests.exceptions import JSONDecodeError
import udi_interface
import time

API_URL = 'https://developer-api.govee.com/v1/'
api_key = ''

MAX_RETRIES = 5

LOGGER = udi_interface.LOGGER

def init(key):
    global api_key

    api_key = key

def get(url):
    code = 0
    retries = 0

    while code != 200 and retries < MAX_RETRIES:
        res = requests.get(API_URL + url, headers={
            'accept': 'application/json',
            'Govee-API-Key': api_key
        })
        code = res.status_code

        if code == 429:
            time.sleep(int(res.headers['Retry-After']) + 1)

        retries += 1

    try:
        parsed = res.json()
        return parsed
    except JSONDecodeError:
        LOGGER.error(f'Failed to decode JSON response: {res.text}')
        return None

def query(url, params):
    code = 0
    retries = 0

    while code != 200 and retries < MAX_RETRIES:
        res = requests.get(API_URL + url, headers={
            'accept': 'application/json',
            'Govee-API-Key': api_key
        }, params=params)
        code = res.status_code

        if code == 429:
            time.sleep(int(res.headers['Retry-After']) + 1)

        retries += 1

    try:
        parsed = res.json()
        return parsed
    except JSONDecodeError:
        LOGGER.error(f'Failed to decode JSON response: {res.text}')
        return None

def put(url, params):
    code = 0
    retries = 0

    while code != 200 and retries < MAX_RETRIES:
        res = requests.put(API_URL + url, headers={
            'accept': 'application/json',
            'Govee-API-Key': api_key
        }, json=params)
        code = res.status_code

        if code == 429:
            time.sleep(int(res.headers['Retry-After']) + 1)
        retries += 1

    try:
        parsed = res.json()
        return parsed
    except JSONDecodeError:
        LOGGER.error(f'Failed to decode JSON response: {res.text}')
        return None
