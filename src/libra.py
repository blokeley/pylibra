#! /usr/bin/env python

"Core libra functions"

import ConfigParser
import logging
import logging.config
import os

def readSerialConfig(configFile):
    if not os.path.isfile(configFile):
        raise Exception(configFile + ' not found.')
    
    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    temp = config.items(serial)
    return config.items(serial)

def startParser():
    self.__filename = 'data.csv'
    print 'Parser started'
    
def stopParser():
    raise NotImplementedError
