#! /usr/bin/env python

"Core libra functions"

import ConfigParser
import logging
import os
import serial

logger = logging.getLogger(__name__)
configFile = 'libra.conf'

def readSerialConfig(configFile):
    if not os.path.isfile(configFile):
        raise IOError(configFile + ' not found.')
    
    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    return config.items('serial')



def startParser(settings=readSerialConfig(configFile)):
    #TODO: implement
    logger.info('Parser started')
    
def stopParser():
    #TODO: implement
    logger.info('Parser stopped')
    raise NotImplementedError

