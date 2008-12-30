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
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'pylibra'))
import utils

import logging
import optparse
import serial
import time

def main():
    # Flush stdout immediately after writing
    sys.stdout = utils.FlushFile(sys.stdout)

    # Use line ending for current system
    DEFAULT_DATA = 'ST 1.23g OK'
    
    # Parse the command line arguments
    argsParser = optparse.OptionParser()
    argsParser.add_option('-p', help='serial port name (%default)', default=0)
    argsParser.add_option('-b', help='baudrate (%default)', default=2400, type='int')
    argsParser.add_option('-i', help='interval (%default)', default=1.0, type='float')
    argsParser.add_option('-d', help='data to send (%default)', default=DEFAULT_DATA)
    argsParser.add_option('-v', help='verbose', action='store_true', default=False)
    options, args = argsParser.parse_args()
    
    # Set logging level
    if options.v: 
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(options)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Get the serial port
    try:
        port = serial.Serial(port=options.p, baudrate=options.b)
    except Exception, ex:
        logging.error(ex)
        sys.exit(1)

    logging.debug('Using port: %s' % port.portstr)
    port.open()
    
    def spew():
        logging.debug('Writing %s' % options.d)
        port.write(options.d + os.linesep)
    
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
