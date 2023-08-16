"""
SensorPush Node Server
Copyright (C) 2023 James Bennett

MIT License
"""

'''
TODO - Add more comments
'''

import udi_interface
import sys
from nodes import controller
import rest
import time

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

'''
Main function for generating nodes at beginning of server
'''

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        Parameters = Custom(polyglot, 'customparams')

        mainNode = controller.Controller(polyglot, 'controller', 'controller', 'Govee Controller')
        
        def parameterHandler(params):
            Parameters.load(params)

            if 'API Key' in Parameters:
                key = Parameters['API Key']

                if key != '':
                    polyglot.Notices.clear()
                    rest.init(Parameters['API Key'])

                    if 'controller' in polyglot.getNodes():
                        mainNode.createDevices()
                else:
                    # No key provided
                    polyglot.Notices['API'] = 'Missing API Key'
            else:
                polyglot.Notices['API'] = 'Missing API Key Parameter'
            
            
        '''
        Handles authorization by using OAuth2 and sensorpush's login portal
        '''

        polyglot.subscribe(polyglot.CUSTOMPARAMS, parameterHandler)


        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()

        polyglot.addNode(mainNode)

        # Just sit and wait for events
        polyglot.ready()
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

