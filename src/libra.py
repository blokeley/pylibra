#! /usr/bin/env python

"""Run the libra data logging program.

use "libra -h" for more help
"""

from optparse import OptionParser
import logging
import logging.config
import sys

def usage(*args):
    "Print usage and exit"
    if args:
        sys.stdout = sys.stderr
        for msg in args: print msg
        print __doc__
    else:
        argsParser.print_help()
    sys.exit(2)

def main():
    "Main program: parse command line and process"
    
    # Set up the root logger
    logging.config.fileConfig('logging.conf')
    logging.info('libra started')
    
    argsParser = OptionParser()
    argsParser.add_option('-f', '--file', dest='settingsFile',
                          help='read settings from settingsFile', )
    argsParser.add_option("-v", '--verbose', action="store_const", 
                          dest="verbose", const=2,
                          help='print lots of information whilst running')
    argsParser.add_option("-q", '--quiet', action="store_const", 
                          dest="verbose", const=0,
                          help='print no information whilst running')
    argsParser.set_defaults(verbose=1)
    argsParser.set_defaults(settingsFile='serial.conf')
    (options, args) = argsParser.parse_args()
    logging.debug('Options: ' + str(options))
    
    # Override the settings file
    if options.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)
    if options.verbose == 0:
        logging.getLogger().setLevel(logging.WARNING)
        
    # Read the settings file
    # TODO: Read how Python deals with properties files
    
if '__main__' == __name__:
    main()
