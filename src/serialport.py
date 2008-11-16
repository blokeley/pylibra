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

"Serial port functions."

from __future__ import with_statement
import copy
import threading
import logging
import serial
import time

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig()

# Sleep between reads in seconds
delay = 0.5

class SerialReader(threading.Thread):
    
    def __init__(self, *callbacks, **settings):
        """Set up serial reader.
        
        settings is a dict containing the serial port settings. See 
                 http://pyserial.wiki.sourceforge.net/pySerial
        callbacks is a list of the functions to call when data is received
        """
        
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when spawning thread dies
        self.__lock = threading.RLock()
        self.port = None
        
        if not callbacks:
            logger.warning('Serial port has no observers')
        else:
            # Use slicing to make a copy
            self.__callbacks = copy.deepcopy(callbacks)
        
        if not settings:
            raise ValueError, 'No serial port settings given.'
        
        self.settings = copy.deepcopy(settings)
    
    def __checkSerial(self):
        # ONLY CALL WHILST HOLDING self.__lock
        try:
            if not self.port:
                self.port = serial.Serial(**self.settings)
                
            numChars = self.port.inWaiting()
            
            # Read the port
            if (numChars > 0):
                input = self.port.read(numChars)
                
                # Send the data to listeners
                for callback in self.__callbacks:
                    callback(input)
                
        except serial.SerialException, ex:
            logger.warning(str(ex))

    def stop(self):
        with self.__lock:
            portname = self.port.portstr
            self.__stopRequested = True
            if self.port:
                self.port.flushInput()
                self.port.close()
            
        logger.info('Closed port ' + portname)
        
    def run(self):
        with self.__lock:
            self.__stopRequested = False
        
        # Cycle polling the port
        while True:
            with self.__lock:
                if self.__stopRequested:
                    break
                self.__checkSerial()    
            time.sleep(delay)
