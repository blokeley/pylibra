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

"Unit tests for fileio module."

from wx.tools.Editra.src.ed_main import __name__
import csv
import os
import unittest

import fileio

class TestFileIO(unittest.TestCase):
    
    def setUp(self):
        self.__filename = 'data.csv'
        if os.path.isfile(self.__filename):
            os.remove(self.__filename)
            
    def testWrite(self):
        "Tests fileio.write() method."
        
        row = [str(x) for x in range(10)]
        data = [row]
        fileio.save(data)
        dataReader = csv.reader(open('data.csv'))
        result = []
        for row in dataReader:
            result.append(row)
        
        self.assertEqual(result, data)

if __name__ == '__main__':
    unittest.main()
