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

"Unit tests for model module."

import model

import unittest

class TestModel(unittest.TestCase):
    "Unit test for Model class."
    
    def setUp(self):
        self.cols = ['ID', 'Value', 'Unit', 'Remarks']
    
    def testAddRow(self):
        myModel = model.Model(self.cols)
        data = (1, 12.3, 'grams', 'First data')
        myModel.addRow(data)
        self.assertEqual(data, myModel.data[0])

    def testRemoveRow(self):
        myModel = model.Model(self.cols)
        data = (1, 12.3, 'grams', 'First data')
        myModel.addRow(data)
        self.assertEqual(data, myModel.data[0])
        myModel.removeRow(0)
        self.assertEqual([], myModel.data)
        
    def testManyRemoveRow(self):
        myModel = model.Model(self.cols)
        data = (1, 12.3, 'grams', 'First data')
        myModel.addRow(data)
        myModel.addRow((2, 12.3, 'grams', 'First data'))
        myModel.addRow((3, 12.3, 'grams', 'First data'))
        myModel.removeRow(1)
        expectedData = [(1, 12.3, 'grams', 'First data'), 
                        (3, 12.3, 'grams', 'First data')]
        self.assertEqual(expectedData, myModel.data)
   
if '__main__' == __name__:
    unittest.main()
