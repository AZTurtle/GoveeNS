"""
SensorPush Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

import udi_interface
import sys
import rest

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

'''
This is the sensor node class.
It's just a node for storing data, no actions.
'''
class Light(udi_interface.Node):
    id = 'child'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 2}
            ]

    def __init__(self, polyglot, parent, address, name, api_address, model):
        super(Light, self).__init__(polyglot, parent, address, name)

        self.poly = polyglot
        self.api_address = api_address
        self.model = model

        polyglot.subscribe(polyglot.POLL, self.poll)

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            state = rest.query('devices/state', {
                'device': self.api_address,
                'model': self.model
            })['data']

            self.setDriver('ST', state['properties'][0], True, True)
            self.setDriver('GV0', state['properties'][1], True, True)