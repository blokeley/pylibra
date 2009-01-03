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

'Entry point for using text (command line) user interface.'
import libra
import utils

import logging
import logging.config
import optparse
import os
import sys
import time

logger = logging.getLogger(__name__)
helpMessage = 'Type q to quit:'

def dataCallback(data):
    'Called when data is successfully parsed.'
    for row in data:
        print time.strftime('%Y-%m-%d %H:%M:%S'), row

def main():
    'Main program: parse command line and process.'
    # Make stdout write almost immediately
    sys.stdout = utils.FlushFile(sys.stdout)

    # Parse the command line options
    argsParser = optparse.OptionParser(version=libra.VERSION)
    argsParser.add_option('-o', '--outfile', dest='outfile',
                          help='output data to outfile (%default)',
                          default='data.csv')
    options, args = argsParser.parse_args()

    # Set up logging
    logging.config.fileConfig('logging.cfg')
    logger.debug('Options: ' + str(options))

    # Backup the old data file if it exists
    if os.path.isfile(options.outfile):
        backup = options.outfile + '.bak'
        if os.path.isfile(backup): os.remove(backup)
        os.rename(options.outfile, backup)
    
    # Read the settings file
    app = libra.Libra(dataCallback)

    # Start the parser
    app.startParser()
    
    # Print a message on how to quit
    print helpMessage
    
    # Block until quit command is received
    while sys.stdin.readline()[0] != 'q':
        print helpMessage
    
    # Stop the parser
    app.stopParser()
    print 'Quitting.'
    
if '__main__' == __name__:
    main()
