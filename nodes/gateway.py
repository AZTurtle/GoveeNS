#!/usr/bin/env python3
"""
Polyglot v3 node server Example 3
Copyright (C) 2021 Robert Paauwe

MIT License
"""
import udi_interface
import sys
import time
from nodes import sensor
import rest

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

'''
Controller is interfacing with both Polyglot and the device. In this
case the device is just a count that has two values, the count and the count
multiplied by a user defined multiplier. These get updated at every
shortPoll interval.
'''
class Controller(udi_interface.Node):
    id = 'ctl'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2}
            ]

    def __init__(self, polyglot, parent, address, name, sensor_list, start_num):
        super(Controller, self).__init__(polyglot, parent, address, name)

        self.poly = polyglot
        self.count = 0
        self.n_queue = []
        self.sensor_list = sensor_list
        self.num = start_num

        # subscribe to the events we want
        
        polyglot.subscribe(polyglot.START, self.start, address)
        polyglot.subscribe(polyglot.STOP, self.stop)
        polyglot.subscribe(polyglot.POLL, self.poll)
        polyglot.subscribe(polyglot.ADDNODEDONE, self.node_queue)

        # start processing events and create add our controller node

    

    '''
    node_queue() and wait_for_node_event() create a simple way to wait
    for a node to be created.  The nodeAdd() API call is asynchronous and
    will return before the node is fully created. Using this, we can wait
    until it is fully created before we try to use it.
    '''

    '''
    This is called when the node is added to the interface module. It is
    run in a separate thread.  This is only run once so you should do any
    setup that needs to be run initially.  For example, if you need to
    start a thread to monitor device status, do it here.

    Here we load the custom parameter configuration document and push
    the profiles to the ISY.
    '''

    '''
    Create the children nodes.  Since this will be called anytime the
    user changes the number of nodes and the new number may be less
    than the previous number, we need to make sure we create the right
    number of nodes.  Because this is just a simple example, we'll first
    delete any existing nodes then create the number requested.
    '''

    def node_queue(self, data):
        self.n_queue.append(data['address'])

    def wait_for_node_done(self):
        while len(self.n_queue) == 0:
            time.sleep(0.1)
        self.n_queue.pop()

    def defineSensors(self):

        self.sensors = {}

        for i in self.sensor_list:
            try:
                node = sensor.SensorNode(self.poly, self.address, f'child_{self.num}', i[1])
                self.poly.addNode(node)
                self.sensors[i[0]] = node
                self.wait_for_node_done()
                self.num += 1
            except Exception as e:
                LOGGER.error('Error when creating sensor: {}'.format(e))


    def poll(self, polltype):
        nodes = self.poly.getNodes()

        if 'shortPoll' in polltype:
            samples = rest.post('samples', {
                'limit': self.sample_num
            })

            sensors = samples['sensors']

            for sample in sensors:

                if sample not in self.sp_nodes:
                    #Add node
                    LOGGER.info(f'{sample} node not found... Creating!')
                    continue
                else:
                    sensor_ = sensors[sample]
                    address = self.sp_nodes[sample]
                    nodes[address].setDriver('GV0', int(sensor_[0]['temperature']), True, True)
                    nodes[address].setDriver('GV1', int(sensor_[0]['humidity']), True, True)

    def start(self):  
        self.defineSensors()
        LOGGER.debug(self.sensors)

    '''
    Change all the child node active status drivers to false
    '''
    def stop(self):

        nodes = self.poly.getNodes()
        for node in nodes:
            if node != 'controller':   # but not the controller node
                nodes[node].setDriver('ST', 0, True, True)

        self.poly.stop()
