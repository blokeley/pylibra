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
import utils

# Standard modules
import ConfigParser
import logging
import os
import serial

class Libra(object):
    "Main application class that can be run from text ui or gui."
    
    def __init__(self, *dataCallbacks):
        self.__logger = logging.getLogger(__name__)
        self.port = None
        self.timer = None
        assert dataCallbacks, 'Must have at least one callback to do anything'
        self.dataCallbacks = dataCallbacks
    
    def readSerialConfig(self, configFile=None):
        "Reads configuration from given file."
        
        if not configFile: configFile = 'libra.cfg'
        # Try given config file
        if not os.path.isfile(configFile):
            raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        settings = dict(config.items('serial'))
        return settings
    
    def poll(self):
         bytes = self.port.inWaiting()
         self.__logger.debug('%d bytes waiting' % bytes)
         if bytes: 
             data = self.port.read(bytes)
             self.parser.parse(data)
    
    def startParser(self, *callbacks, **settings):
        "Starts parser listening for serial data."
        if not settings: settings = self.readSerialConfig()
        self.__logger.info('Parser starting')

        try:
            self.port = serial.Serial(settings['port'])
        except serial.SerialException, msg:
            self.__logger.warning(msg)
            return
        
        self.parser = parsing.Parser(settings['regex'], self.dataCallbacks)
        
        if not self.timer: 
            self.timer = utils.PeriodicTimer(1, self.poll)
        self.__logger.debug('Starting timer...')
        self.timer.start()
        self.__logger.debug('Timer started.')
        
    def stopParser(self):
        self.__logger.info('Parser stopping')
        if self.timer: self.timer.end()
