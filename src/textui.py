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

"Entry point for using text (command line) user interface."

import libra

import logging
import logging.config
import optparse
import sys
import time

logger = logging.getLogger(__name__)

def dataCallback(data):
    "Called when data is successfully parsed."
    print time.strftime('%Y-%m-%d %H:%M:%S'), data

def main():
    "Main program: parse command line and process"
    
    # Set up the root logger
    logger.info('libra started')
    
    argsParser = optparse.OptionParser()
    argsParser.add_option('-c', '--config', dest='configFile',
                          help='read settings from configFile', 
                          default='libra.cfg')
    argsParser.add_option('-o', '--outfile', dest='outFile',
                          help='output data to outFile', 
                          default='data.csv')
    argsParser.add_option('-l', '--logconfig', dest='logConfig',
                          help='read logging settings from logConfigFile',
                          default='logging.cfg')
    (options, args) = argsParser.parse_args()
    logging.config.fileConfig(options.logConfig)
    logger.debug('Options: ' + str(options))
    
    # Read the settings file
    app = libra.Libra(dataCallback)
    serialSettings = app.readSerialConfig(options.configFile)
    app.startParser(serialSettings)
    
    while (True):
        print 'Type q to quit:',
        input = sys.stdin.readline()
        if input[0] == 'q':
            print 'Quitting..,'
            app.stopParser()
            break
        time.sleep(2)
    
if '__main__' == __name__:
    main()

