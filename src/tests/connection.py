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

import unittest, serial, logging, time

class TestConnection(unittest.TestCase):
    "Quick test to check serial port."
    
    _msg = 'Hello!'
    
    def setUp(self):
        # Open the serial port
        self.readPort = serial.Serial('/dev/ttyUSB0')
        self.writePort = serial.Serial('/dev/ttyUSB1')
        # Clear the ports
        self.readPort.flushInput()
        self.writePort.flushOutput()

    def tearDown(self):
        # Close the serial port
        self.readPort.close()
        self.writePort.close()
        
    def testConn(self):
        self.assertNotEqual(self.readPort, None)
        self.assertNotEqual(self.writePort, None)
        
    def testReadWrite(self):
        self.writePort.write(self._msg)
        time.sleep(0.05) # Wait for serial port
        port = self.readPort
        incoming = port.read(port.inWaiting())
        self.assertEqual(incoming, self._msg)
        
    def testBadReadWrite(self):
        self.writePort.write(self._msg + 'rubbish')
        time.sleep(0.05) # Wait for serial port
        port = self.readPort
        incoming = port.read(port.inWaiting())
        self.assertNotEqual(incoming, self._msg)
        
if '__main__' == __name__:
    print TestConnection.__doc__
    unittest.main()
