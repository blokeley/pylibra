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

"Module for reading and writing data to and from a file."

from __future__ import with_statement
import csv
import logging

def save(data, filename='data.csv'):
    "Saves the data to the given filename"
    
    logging.debug('Saving %s' % filename)
    
    with open(filename, 'w') as outFile:
        writer = csv.writer(outFile)
        writer.writerows(data)
        
    logging.debug('Finished saving %s' % filename)
