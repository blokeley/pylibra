#!/usr/bin/env python
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
# along with pylibra. If not, see http://www.gnu.org/licenses/

"""Entry point for using text (command line) user interface."""

import logging
import logging.config
import optparse
import os
import sys

# Set up logging before user imports
logging.config.fileConfig('logging.cfg')

import core
import utils

_LOGGER = logging.getLogger(__name__)


def echo(lines):
    """Called when data is successfully parsed."""
    # Take last reading only
    line = lines[-1]
    # Timestamp each line
    line = core.timestamp(line)
    print line


def main():
    """Main program entry function.
    
    Parse the command line, process the options and start the parser.
    
    """
    # Make stdout write almost immediately
    sys.stdout = utils.FlushFile(sys.stdout)

    # Parse the command line options
    argsParser = optparse.OptionParser(version=core.__version__)
    argsParser.add_option('-o', '--outfile', dest='outfile',
                          help='output data to outfile (%default)',
                          default='data.csv')
    options = argsParser.parse_args()[0]

    _LOGGER.info('Starting pylibra' + '-' * 30)
    _LOGGER.debug('Options: ' + str(options))

    # Backup the old data file if it exists
    if os.path.isfile(options.outfile):
        backup = options.outfile[:-4] + '.bak'
        if os.path.isfile(backup):
            os.remove(backup)
        os.rename(options.outfile, backup)
    
    # Read the settings file
    app = core.DataManager(options.outfile)
    app.datacallbacks.append(echo)

    columns = core.get_columns()
    if columns:
        core.write_to_file(options.outfile, (columns,))

    # Start the parser
    app.start_parser()
    
    # Block until quit command is received
    while True:
        command = raw_input('Type q to quit:')
        if command[0] == 'q': 
            break
    
    # Stop the parser
    app.stop_parser()
    print 'Quitting.'
    _LOGGER.info('Exit OK.' + '-' * 30)


if '__main__' == __name__:
    try:
        main()
    except Exception:
        _LOGGER.exception('Unhandled exception.')
    finally:
        logging.shutdown()
