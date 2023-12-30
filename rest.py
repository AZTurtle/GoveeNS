"""
Govee Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

import requests
import udi_interface
import time

API_URL = 'https://developer-api.govee.com/v1/'
api_key = ''

LOGGER = udi_interface.LOGGER

def init(key):
    global api_key

    api_key = key

def get(url):
    res = requests.get(API_URL + url, headers={
        'accept': 'application/json',
        'Govee-API-Key': api_key
    })

    LOGGER.debug(res)

    return res.json()

def query(url, params):
    code = 0

    while code != 200:
        res = requests.get(API_URL + url, headers={
            'accept': 'application/json',
            'Govee-API-Key': api_key
        }, params=params)
        code = res.status_code

        LOGGER.debug(res)

        if code == 429:
            time.sleep(int(res.headers['Retry-After']) + 1)

    return res.json()

def put(url, params):
    code = 0

    while code != 200:
        res = requests.put(API_URL + url, headers={
            'accept': 'application/json',
            'Govee-API-Key': api_key
        }, json=params)
        code = res.status_code

        if code == 429:
            time.sleep(int(res.headers['Retry-After']) + 1)


    return res.json()
