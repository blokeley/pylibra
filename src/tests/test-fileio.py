"Unit tests for fileio module."

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
