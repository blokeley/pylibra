#! /usr/bin/env python

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
