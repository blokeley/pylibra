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

'''
Usage: sqlprint.py dbfilename
Utility to print sqlite database contents to stdout.
'''

import os.path
import sqlite3
import sys

def usage(*args):
    'Prints help message.'
    sys.stdout = sys.stderr
    for msg in args: print msg
    print __doc__
    sys.exit(2)

def main():
    if not sys.argv[1:]: usage('Database file not given.')

    file = sys.argv[1]
    if not os.path.isfile(file): usage('Database %s not found.' % file)

    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    # Get the tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

    # Iterate over the tables, printing their contents
    for table in cursor.fetchall():
        print '\nPrinting table: %s' % table[0]
        cursor.execute("SELECT * FROM '%s'" % table[0])
        for row in cursor.fetchall():
            for field in row:
                print field,
            print

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
