#! /usr/bin/env python

"Core libra functions"

# User modules
import parsing

# Standard modules
import ConfigParser
import logging
import os
import serial
import threading
import time

class SerialThread(threading.Thread):
    "Polls for serial data in the background."
    
    def __init__(self, serialPort, parser):
        self.running = True
        self.port = serialPort
        self.parser = parser
        self.__logger = logging.getLogger(__name__)
        
    def run(self):
        # Poll until running is set to false
        self.__logger.debug('Starting serial polling')
        while running:
            bytes = self.port.inWaiting()
            if bytes:
                self.parser.parse(bytes)
            time.sleep(0.5)
        self.__logger.debug('Stopping serial polling.')

class Libra:
    
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.port = None
    
    def readSerialConfig(self, configFile):
        "Reads configuration from given file."
        
        # Try given config file
        if not os.path.isfile(configFile):
            configFile = 'libra.conf'
            if not os.path.isfile(configFile):
                raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        return config.items('serial')
    
    def startParser(settings=readSerialConfig(configFile)):
        "Starts parser listening for serial data."
        self.__logger.info('Parser started')
        self.port = serial.Serial(settings)
        parser = parsing.Parser(settings['regex'], callback)
        serialThread = SerialThread(self.port, )
        
    def stopParser():
        #TODO: implement
        self.__logger.info('Parser stopped')
        raise NotImplementedError

