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

"""Core libra functions."""
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
import time

# Version must be a string but be parsable to float by py2exe.
VERSION='0.3'

def timestamp(mylist):
    """Inserts a timestamp string at the beginning of the given list."""
    mylist = list(mylist)
    mylist.insert(0, time.strftime('%Y-%m-%d %H:%M:%S'))
    return mylist

class Libra(object):
    """Main application class that can be run from text ui or gui."""

    # Interval between polls in seconds
    SERIALPOLLINTERVAL = 1
    
    def __init__(self, filename='data.csv'):
        """Creates the controller.

        filename - the file to write data to
        """ 
        self._logger = logging.getLogger(__name__)
        self.filename = filename
        self.timer = utils.PeriodicTimer(Libra.SERIALPOLLINTERVAL, self.poll)
        self.datacallbacks = [self.writetofile,]

    def readSerialConfig(self, configFile='libra.cfg'):
        """Reads configuration from given file."""
        # Try given config file
        if not os.path.isfile(configFile):
            raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        settings = dict(config.items('serial'))
        return settings
    
    def poll(self):
         """Polls the serial port for data and calls the parser 
         if any is present."""
         if not self.port.isOpen(): self.port.open()
         bytes = self.port.inWaiting()
         self._logger.debug('%d bytes waiting' % bytes)
         if bytes: 
             data = self.port.read(bytes)
             self.parser.parse(data)
    
    def startParser(self, **settings):
        """Starts parser listening for serial data."""
        if not settings: settings = self.readSerialConfig()
        
        # Write the column headings to file
        columns = settings['columns'].split(',')
        # Remove empty column headings
        if '' in columns: columns.remove('')
        self._logger.debug('Columns: %s', columns)
        if columns: self.writetofile((columns,))
        
        self._logger.info('Parser starting')

        try:
            # Set up the serial port
            self.port = serial.Serial(settings['port'],
            int(settings['baudrate']),
            int(settings['bytesize']),
            settings['parity'],
            int(settings['stopbits']))
        except serial.SerialException, msg:
            self._logger.warning(msg)
            return False
        
        try:
            # If config file has a regex, use a RegexParser
            self.parser = parsing.RegexParser(settings['regex'], *self.datacallbacks)
        except KeyError:
            # If no regex is defined, use a WordParser
            self.parser = parsing.WordParser(*self.datacallbacks)

        # Start polling the serial port
        self._logger.debug('Starting timer...')
        self.timer.start()
        
    def stopParser(self):
        """Stops the parser."""
        self._logger.info('Parser stopping')
        self.timer.end()
        try:
            if self.port.isOpen(): self.port.close()
        except AttributeError: pass

    def writetofile(self, data):
        """Writes the data to the given filename.

        data - a sequence of sequences (e.g. a list of lists).
        """
        # Add a timestamp
        newdata = map(timestamp, data)

        logging.debug('Writing to %s; data=%s' % (self.filename, newdata))

        with open(self.filename, 'a') as outFile:
            writer = csv.writer(outFile, lineterminator='\n')
            writer.writerows(newdata)
