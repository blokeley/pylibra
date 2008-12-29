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
import os.path
import serial
import sqlite3
import time

class Libra(object):
    'Main application class that can be run from text ui or gui.'

    # Interval between polls in seconds
    SERIALPOLLINTERVAL = 1
    
    def __init__(self, dataCallbacks):
        '''Creates the controller.
        
        dataCallbacks is a tuple containing functions to call if data is
        received.
        ''' 
        self.__logger = logging.getLogger(__name__)
        self.port = None
        self.timer = None
        self.db = Database()
        assert dataCallbacks, 'Must have at least one callback to do anything'
        self.dataCallbacks = [self.db.storeData, dataCallbacks]
    
    def readSerialConfig(self, configFile=None):
        'Reads configuration from given file.'
        
        if not configFile: configFile = 'libra.cfg'
        # Try given config file
        if not os.path.isfile(configFile):
            raise IOError(configFile + ' not found.')
        
        config = ConfigParser.SafeConfigParser()
        config.read(configFile)
        settings = dict(config.items('serial'))
        return settings
    
    def poll(self):
         'Polls the serial port for data and calls the parser if any is present.'
         bytes = self.port.inWaiting()
         self.__logger.debug('%d bytes waiting' % bytes)
         if bytes: 
             data = self.port.read(bytes)
             self.parser.parse(data)
    
    def startParser(self, *callbacks, **settings):
        'Starts parser listening for serial data.'
        if not settings: settings = self.readSerialConfig()
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
            return
        
        self.parser = parsing.Parser(settings['regex'], *self.dataCallbacks)
        
        if not self.timer: 
            self.timer = utils.PeriodicTimer(Libra.SERIALPOLLINTERVAL, self.poll)
        self.__logger.debug('Starting timer...')
        self.timer.start()
        
    def stopParser(self):
        'Stops the parser'
        self.__logger.info('Parser stopping')
        if self.timer: self.timer.end()
        if self.port:
            if self.port.isOpen():
                self.port.close()

class Database(object):
    '''Handles database creation and access.

    filename is the relative path to the desired database file.
    columns is a sequence of the column names.
    '''
    
    def __init__(self, columns, filename='libra.dat'):
        self._columns = columns
        self._filename = filename

        # Create a queue for database functions to be called on
        # (sqlite does not support multithreading)
        self._serializer = utils.Serializer()

    # Filename property
    def _getFilename(self): return self._filename
    FILENAME = property(_getFilename) # Read-only property

    # Columns property
    def _getColumns(self): return self._columns    
    COLUMNS = property(_getColumns) # Read-only property

    def __enter__(self):
        '''Enter the database runtime context.

        See documentation for the "with statement".
        '''
        self._conn = self._serializer.execute(self._connect)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''Exit the database runtime context.

        See documentation for the "with statement".
        '''
        if traceback is None:
            # No exception so commit
            self._serializer.execute(self._conn.commit)
            self._serializer.execute(self._conn.close)
            return True # No exception to return
        else:
            # Exception occured so rollback
            self._serializer.execute(self._conn.rollback)
            self._serializer.execute(self._conn.close)
            return False # Context manager will re-raise any exception

    def _connect(self):
        'Creates the database and returns a connection to it.'
        isnewdb = not os.path.isfile(self.FILENAME)

        # Connect to the database
        conn = sqlite3.connect(self.FILENAME)

        # If the database is new, create the table
        if isnewdb:
            cursor = conn.cursor()

            # TODO: Read table format from config file
            cursor.execute('CREATE TABLE data (date text, status text, other text)')
        return conn

    def insert(self, results):
        '''Stores received data in the database.

        len(results) must equal len(columns)
        '''
        print results
        def store():
            # Create the current timestamp
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor = self._conn.cursor()

            for row in results:
                data = [now]
                for field in row: data.append(field)
                print 'data: %s' % data
                # TODO: Make SQL statement expand to fit results
                cursor.execute('INSERT INTO data VALUES (?,?,?)', data)

        self.serializer.execute(store)

    def select(self):
        'Returns a sequence of sequences representing the data table.'
        def load():
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM data")
            data = []
            for row in cursor:
                data.append(row)
            return data

        return self.serializer.execute(load)
