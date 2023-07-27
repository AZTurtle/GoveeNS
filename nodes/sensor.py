#!/usr/bin/env python3
"""
Polyglot v3 node server Example 3
Copyright (C) 2021 Robert Paauwe

MIT License
"""
import udi_interface
import sys

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

'''
This is our Counter device node.  All it does is update the count at the
poll interval.
'''
class SensorNode(udi_interface.Node):
    id = 'child'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 56},
            {'driver': 'GV1', 'value': 0, 'uom': 56},
            {'driver': 'GV2', 'value': 1, 'uom': 2}
            ]

    def __init__(self, polyglot, parent, address, name):
        super(SensorNode, self).__init__(polyglot, parent, address, name)

        self.poly = polyglot
        self.count = 0

        self.Parameters = Custom(polyglot, 'customparams')

        # subscribe to the events we want
        polyglot.subscribe(polyglot.CUSTOMPARAMS, self.parameterHandler)
        polyglot.subscribe(polyglot.POLL, self.poll)

    '''
    Read the user entered custom parameters. In this case, it is just
    the 'multiplier' value that we want.  
    '''
    def parameterHandler(self, params):
        self.Parameters.load(params)

    '''
    This is where the real work happens.  When we get a shortPoll, increment the
    count, report the current count in GV0 and the current count multiplied by
    the user defined value in GV1. Then display a notice on the dashboard.
    '''
    def poll(self, polltype):

        if 'shortPoll' in polltype:
            if int(self.getDriver('GV2')) == 1:
                LOGGER.debug(f'{self.name} Incrementing...')
                if self.Parameters['multiplier'] is not None:
                    mult = int(self.Parameters['multiplier'])
                else:
                    mult = 1

                self.count += 1

                self.setDriver('GV0', self.count, True, True)
                self.setDriver('GV1', (self.count * mult), True, True)

                # be fancy and display a notice on the polyglot dashboard
                self.poly.Notices[self.name] = '{}: Current count is {}'.format(self.name, self.count)
            else:
                LOGGER.debug(f'{self.name} NOT Incrementing...')

    def set_increment(self,val=None):
        # On startup this will always go back to true which is the default, but how do we restort the previous user value?
        LOGGER.debug(f'{self.address} val={val}')
        self.setDriver('GV2',val)

    def cmd_set_increment(self,command):
        val = int(command.get('value'))
        LOGGER.debug(f'{self.address} val={val}')
        self.set_increment(val)

    commands = {
        "SET_INCREMENT": cmd_set_increment,
    }