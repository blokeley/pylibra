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

'Utility to write data to the given serial port.'

import os
import sys
# Fiddle module loading path to get utils
sys.path.append(os.path.dirname(os.getcwd()))
import utils

import logging
import optparse
import serial
import time

def main():
    # Set logging level
    logging.getLogger().setLevel(logging.INFO)

    # Flush stdout immediately after writing
    sys.stdout = utils.FlushFile(sys.stdout)

    # Use line ending for current system
    DEFAULT_DATA = 'ST 1.23g OK' + os.linesep
    
    # Parse the command line arguments
    argsParser = optparse.OptionParser()
    argsParser.add_option('-p', help='serial port name (%default)', default=0)
    argsParser.add_option('-b', help='baudrate (%default)', default=2400)
    argsParser.add_option('-i', help='interval (%default)', default=1)
    argsParser.add_option('-d', help='data to send (%default)', default=DEFAULT_DATA)
    options, args = argsParser.parse_args()
    logging.debug(options)
    
    # Get the serial port
    port = serial.Serial(port=options.p, baudrate=options.b)
    logging.debug('Using port: %s' % port.portstr)
    port.open()
    
    def spew():
        logging.debug('Writing %s' % options.d)
        port.write(options.d)
    
    # Start writing data
    logging.debug('Starting writer thread...')
    timer = utils.PeriodicTimer(options.i, spew)
    timer.start()
    
    print 'Type q to quit:'
    
    # Listen for quit signal
    while(sys.stdin.readline()[0] != 'q'):
        print 'Type q to quit:'

    # Quit
    print 'Quitting...'
    timer.end()                 # Stop the timer
    time.sleep(1.1 * options.i)
    port.close()
    
if __name__ == '__main__':
    main()
