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

"Unit tests for serialport module."

import unittest
import serial
import time

import serialport

# Time to wait in seconds
delay = 1

def callback(arg):
    "Dummy callback to help testing."
    return arg

class TestSerialport(unittest.TestCase):
    
    def setUp(self):
        self.callbacks = [callback]
        self.settings = {'port':'COM8', 'baudrate':2400}
        
    def testDictToSerial(self):
        port = serial.Serial(**self.settings)
        self.assertEqual(self.settings['port'], port.portstr)
        port.close()
        #port = serial.Serial(**self.settings) # check that port can reopen
        
    
    def testStart(self):
        reader = serialport.SerialReader(*self.callbacks, 
                                         **self.settings)
        reader.start()
        time.sleep(delay)
        reader.stop()
        
if '__main__' == __name__:
    unittest.main()
