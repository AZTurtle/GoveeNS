"""
SensorPush Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

import requests
import udi_interface

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
    return requests.get(API_URL + url, headers={
        'accept': 'application/json',
        'Govee-API-Key': api_key
    }, params=params).json()

def put(url, params):
    return requests.put(API_URL + url, headers={
        'accept': 'application/json',
        'Govee-API-Key': api_key
    }, json=params).json()
