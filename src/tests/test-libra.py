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

"Unit tests for libra module."
from __future__ import with_statement
import libra
import os
import unittest

class TestDatabase(unittest.TestCase):
    
    FILENAME = 'test.dat'

    def setUp(self):
        if os.path.isfile(TestDatabase.FILENAME):
            os.remove(TestDatabase.FILENAME)

    def tearDown(self):
        if os.path.isfile(TestDatabase.FILENAME):
            os.remove(TestDatabase.FILENAME)

    def testFileCreated(self):
        with libra.Database((None,), TestDatabase.FILENAME): pass
        self.assertTrue(os.path.isfile(TestDatabase.FILENAME))
        
    def testColumnsCreated(self):
        cols = ('Col1', 'Col2')
        with libra.Database(cols, TestDatabase.FILENAME) as db:
            self.assertEqual(cols, db.COLUMNS)

#    def testStore2By2Table(self):
#        data = (
#        ('row1col1', 'row1col2'),
#        ('row2col1', 'row2col2')
#        )
#
#        # Store and retrieve the data
#        with libra.Database()
#        self.db.store(data)
#        results = self.db.load()
#
#        for i, row in enumerate(results):
#            # Ignore first column because it is a timestamp
#            self.assertEqual(data[i], row[1:])

#    def testStore3By3Table(self):
#        data = (
#        ('row1col1', 'row1col2', 'row1col3'),
#        ('row2col1', 'row2col2', 'row2col3'),
#        ('row3col1', 'row3col2', 'row3col3')
#        )
#
#        # Store and retrieve the data
#        self.db.store(data)
#        results = self.db.load()
#
#        for i, row in enumerate(results):
#            # Ignore first column because it is a timestamp
#            self.assertEqual(data[i], row[1:])

if __name__ == "__main__":
    unittest.main()
