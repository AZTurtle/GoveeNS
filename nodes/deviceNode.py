"""
SensorPush Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

import udi_interface
import sys

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
            {'driver': 'GV0', 'value': 0, 'uom': 17},
            {'driver': 'GV1', 'value': 0, 'uom': 51},
            {'driver': 'GV2', 'value': 0, 'uom': 72}
            ]

    def __init__(self, polyglot, parent, address, name, api_address):
        super(Light, self).__init__(polyglot, parent, address, name)

        self.poly = polyglot
        self.api_address = api_address