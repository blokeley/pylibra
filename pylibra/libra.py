#! /usr/bin/env python
#
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

'Core libra functions'

from __future__ import with_statement
# User modules
import parsing
import utils

# Standard modules
import ConfigParser
import csv
import logging
import os
import serial

VERSION='v0.1'

class Libra(object):
    'Main application class that can be run from text ui or gui.'

    # Interval between polls in seconds
    SERIALPOLLINTERVAL = 1
    
    def __init__(self, *dataCallbacks):
        '''Creates the controller.

        Attributes:
            dataCallbacks -- a tuple containing functions to call if data is received.
        ''' 
        self.__logger = logging.getLogger(__name__)
        self.timer = utils.PeriodicTimer(Libra.SERIALPOLLINTERVAL, self.poll)

        # TODO: Handle custom output files
        self.dataCallbacks = [write,]
        if dataCallbacks: self.dataCallbacks.append(*dataCallbacks)
    
    def readSerialConfig(self, configFile='libra.cfg'):
        'Reads configuration from given file.'
        # Try given config file
        if not os.path.isfile(configFile):
            raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        settings = dict(config.items('serial'))
        return settings
    
    def poll(self):
         'Polls the serial port for data and calls the parser if any is present.'
         if not self.port.isOpen(): self.port.open()
         bytes = self.port.inWaiting()
         self.__logger.debug('%d bytes waiting' % bytes)
         if bytes: 
             data = self.port.read(bytes)
             self.parser.parse(data)
    
    def startParser(self, **settings):
        'Starts parser listening for serial data.'
        if not settings: settings = self.readSerialConfig()
        
        # Write the column headings to file
        columns = settings['columns'].split(',')
        columns.remove('')
        self.__logger.debug('Columns: %s', columns)
        if columns: write((columns,))
        
        self.__logger.info('Parser starting')

        try:
            # Set up the serial port
            self.port = serial.Serial(settings['port'],
            int(settings['baudrate']),
            int(settings['bytesize']),
            settings['parity'],
            int(settings['stopbits']))
        except serial.SerialException, msg:
            self.__logger.warning(msg)
            return False
        
        try:
            # If config file has a regex, use a RegexParser
            self.parser = parsing.RegexParser(settings['regex'], *self.dataCallbacks)
        except KeyError:
            # If no regex is defined, use a WordParser
            self.parser = parsing.WordParser(*self.dataCallbacks)

        # Start polling the serial port
        self.__logger.debug('Starting timer...')
        self.timer.start()
        
    def stopParser(self):
        'Stops the parser.'
        self.__logger.info('Parser stopping')
        self.timer.end()
        if self.port.isOpen(): self.port.close()

def write(data, filename='data.csv'):
    '''Writes the data to the given filename.

    Attributes:
        data -- a sequence of sequences (e.g. a list of lists).
        filename -- any file that can be opened.
    '''
    logging.debug('Writing to %s; data=%s' % (filename, data))

    with open(filename, 'a') as outFile:
        writer = csv.writer(outFile, lineterminator='\n')
        writer.writerows(data)
