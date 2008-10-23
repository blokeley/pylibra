#! /usr/bin/env python

"Entry point for using text (command line) user interface."

from optparse import OptionParser
import logging
import logging.config
import sys

import libra

def main():
    "Main program: parse command line and process"
    
    # Set up the root logger
    logging.info('libra started')
    
    argsParser = OptionParser()
    argsParser.add_option('-c', '--config', dest='configFile',
                          help='read settings from configFile', 
                          default='libra.conf')
    argsParser.add_option('-o', '--outfile', dest='outFile',
                          help='output data to outFile', 
                          default='data.csv')
    argsParser.add_option('-l', '--logconfig', dest='logConfig',
                          help='read logging settings from logConfigFile',
                          default='logging.conf')
    (options, args) = argsParser.parse_args()
    logging.config.fileConfig(options.logConfig)
    logging.debug('Options: ' + str(options))
    
    # Read the settings file
    serialSettings = libra.readSerialConfig(options.configFile)
    libra.startParser(serialSettings)
    
if '__main__' == __name__:
    main()
