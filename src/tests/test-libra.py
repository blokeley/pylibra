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

'Unit tests for libra module.'
from __future__ import with_statement
import libra

import csv
import os
import unittest

class TestWritetofile(unittest.TestCase):

    def setUp(self):
        self._FILENAME = 'data.csv'
        if os.path.isfile(self._FILENAME): os.remove(self._FILENAME)

    def tearDown(self):
        if os.path.isfile(self._FILENAME): os.remove(self._FILENAME)

    def testWrite(self):
        'Tests fileio.write() method.'

        row = [str(x) for x in range(10)]
        inputdata = [row]
        libra.write(inputdata, self._FILENAME)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        self.assertEqual(result, inputdata)

    def testMultipleRows(self):
        'Tests multiple rows.'
        row = [str(x) for x in range(10)]
        inputdata = [row, row]
        libra.write(inputdata, self._FILENAME)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        self.assertEqual(result, inputdata)

    def testMultipleWrites(self):
        'Tests multiple writes.'
        row = [str(x) for x in range(10)]
        inputdata = [row]
        libra.write(inputdata, self._FILENAME)
        libra.write(inputdata, self._FILENAME)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        self.assertEqual(result, [row, row])

if __name__ == "__main__":
    unittest.main()
