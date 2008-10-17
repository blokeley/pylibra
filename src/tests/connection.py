#! /usr/bin/env python
import unittest, serial, logging, time

class TestConnection(unittest.TestCase):
    "Quick test to check serial port."
    
    _msg = 'Hello!'
    
    def setUp(self):
        # Open the serial port
        self.readPort = serial.Serial('COM8')
        self.writePort = serial.Serial('COM9')
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
