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
import sys
import time

# Version must be a string but be parsable to float by py2exe.
VERSION='0.3'

def timestamp(mylist):
    """Inserts a timestamp string at the beginning of the given list."""
    mylist = list(mylist)
    mylist.insert(0, time.strftime('%Y-%m-%d %H:%M:%S'))
    return mylist

def readSerialConfig(configFile='libra.cfg'):
    """Reads configuration from given file."""
    # Try given config file
    if not os.path.isfile(configFile):
        raise IOError(configFile + ' not found.')

    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    try:
        settings = dict(config.items('serial'))
    except ConfigParser.NoSectionError, e:
        print 'Check your config file: '
        for error in e.args: print error
        sys.exit(2)
    return settings

def getColumns(**settings):
    """Returns the data column names."""
    if not settings: settings = readSerialConfig()

    # Get the column headings
    # TODO: use settings.get() to provide a default empty list
    columns = settings['columns'].split(',')

    # Remove empty column headings
    if '' in columns: columns.remove('')
    return columns

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
        self.datacallbacks = [self.write,]

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
        self.stopParser()
        if not settings: settings = readSerialConfig()
        
        self._logger.info('Parser starting')

        try:
            # Set up the serial port
            self.port = serial.Serial(settings['port'],
            int(settings.get('baudrate', 2400)),
            int(settings.get('bytesize', serial.EIGHTBITS)),
            settings.get('parity', serial.PARITY_NONE),
            int(settings.get('stopbits', serial.STOPBITS_ONE)))
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
        self.timer = utils.PeriodicTimer(Libra.SERIALPOLLINTERVAL, self.poll)
        self.timer.start()
        
    def stopParser(self):
        """Stops the parser."""
        self._logger.info('Parser stopping')
        try:
            self.timer.end()
            self.port.close()
        except: pass

    def write(self, data):
        writetofile(self.filename, data)

def writetofile(filename, data):
    """Writes the data to the given filename.

    filename - the filename to write to
    data - a sequence of sequences (e.g. a list of lists).
    """
    # Take last reading only
    lastdata = data[-1]

    # Add a timestamp
    lastdata = timestamp(lastdata)

    with open(filename, 'a') as outFile:
        writer = csv.writer(outFile, lineterminator='\n')
        writer.writerow(lastdata)
