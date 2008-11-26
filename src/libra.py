#! /usr/bin/env python

# Copyright 2008 Tom Oakley 
# This file is part of pylibra.
#
# pylibra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylibra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibra.  If not, see <http://www.gnu.org/licenses/>.

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

class RepeatTimer(threading._Timer):
    "Timer thread to run the arguments given to the constructor."
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        "Runs when instance.start() is called."
        while True:
            self.finished.clear()
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Libra:
    "Main application class that can be run from text ui or gui."
    
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.port = None
        self.timer = None
    
    def readSerialConfig(self, configFile=None):
        "Reads configuration from given file."
        
        if not configFile: configFile = 'libra.cfg'
        # Try given config file
        if not os.path.isfile(configFile):
            raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        # TODO: Convert list of tuples to dict before returning
        settings = dict(config.items('serial'))
        return settings
    
    def poll(self):
         bytes = self.port.inWaiting()
         if bytes: 
             data = self.port.read(bytes)
             self.parser.parse(data)
    
    def startParser(self, settings=None):
        "Starts parser listening for serial data."
        if not settings: settings = self.readSerialConfig()
        self.__logger.info('Parser starting')
        self.port = serial.Serial(settings['port'])
        parser = parsing.Parser(settings['regex'], callback)
        # TODO: Change threading.Timer() to RepeatTimer()
        if not self.timer: self.timer = threading.Timer(0.5, poll)
        self.timer.start()
        
    def stopParser(self):
        #TODO: implement stop()
        self.__logger.info('Parser stopping')
        self.timer.cancel()
