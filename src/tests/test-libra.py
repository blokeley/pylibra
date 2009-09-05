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

"""Unit tests for libra module."""
from __future__ import with_statement
import csv
import logging
import os
import sys
import unittest

# Add pylibra to module loading path
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'pylibra'))
import libra


class TestWritetofile(unittest.TestCase):

    def setUp(self):
        self._FILENAME = 'data.csv'
        if os.path.isfile(self._FILENAME): os.remove(self._FILENAME)

        self.row = [str(x) for x in range(10)]
        self.stampedrow = libra.timestamp(self.row[:])

    def tearDown(self):
        if os.path.isfile(self._FILENAME): os.remove(self._FILENAME)

    def test_write(self):
        """Tests fileio.write() method."""
        inputdata = [self.row]
        core = libra.Libra(self._FILENAME)
        core.write(inputdata)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        self.assertEqual(result, [self.stampedrow,])

    def test_multiple_rows(self):
        """Tests multiple rows in 1 write."""
        # The first row should be rejected because we only write the last
        # complete row of data to disk
        inputdata = [self.row, self.row]
        core = libra.Libra(self._FILENAME)
        core.write(inputdata)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        # Remember, only 1 row (the last) should be written to disk
        expected = [self.stampedrow,]

        self.assertEqual(result, expected)

    def test_multiple_writes(self):
        """Tests multiple writes."""
        inputdata = [self.row]
        core = libra.Libra(self._FILENAME)
        core.write(inputdata)
        core.write(inputdata)

        with open(self._FILENAME) as f:
            dataReader = csv.reader(f)
            result = []
            for row in dataReader:
                result.append(row)

        self.assertEqual(result, [self.stampedrow, self.stampedrow])

if __name__ == "__main__":
    unittest.main()
