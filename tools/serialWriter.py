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

"Utility to write data to the given serial port."

import logging
import optparse
import serial
import threading
import time

def repeat(event, delay, action):
    'Repeats the given action repeatedly until event is set.'
    while True:
        event.wait(delay)       # Wait
        if event.isSet(): break # Quit repeating if requested
        action()                # Perform the action

def main():
    logging.getLogger().setLevel(logging.INFO)
    
    # Parse the command line arguments
    argsParser = optparse.OptionParser()
    argsParser.add_option('-p', help='serial port name', default=0)
    argsParser.add_option('-b', help='baudrate', default=2400)
    argsParser.add_option('-i', help='interval', default=1)
    argsParser.add_option('-d', help='data to send', default='ST 1.23g OK')
    (options, args) = argsParser.parse_args()
    logging.debug(options)
    
    # Get the serial port
    port = serial.Serial(port=options.p, baudrate=options.b)
    logging.info('Using port: %s' % port.portstr)
    
    def write():
        'Writes data to the given port.'
        if not port.isOpen(): port.open()
        try:
            print '%s: %s' % (time.strftime('%S'), options.d )
            #port.write(options.d)
        finally:
            port.close()
    
    # Start writing data
    logging.info('Starting writer thread...')
    event = threading.Event()
    repeatThread = threading.Thread(target=repeat, args=(event, options.i, write))
    repeatThread.start()
    
    # Listen for quit signal
    time.sleep(20)
    event.set()                 # Stop the repeater
    logging.info('Waiting for writer thread to stop...')
    repeatThread.join()
    logging.info('Quitting...')
    
if __name__ == '__main__':
    main()

