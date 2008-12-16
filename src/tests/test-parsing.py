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

import parsing

import unittest

def callback(data):
    global result
    result = data

class TestParsing(unittest.TestCase):
    "Tests parsing classes and functions."
    
    def setUp(self):
        self.regex = r'(ST|OL)\s*(\d+\.\d+)\s*(\S?)'
        self.parser = parsing.Parser(self.regex)
        self.input = 'x ST 12.34 g x'
    
    def tearDown(self):
        self.parser = None
        result = None
    
    def testInitialCallback(self):
        self.parser = parsing.Parser(self.regex, callback)
        self.assertTrue([callback], self.parser._callbacks)
        
    def testAddCallback(self):
        self.assertEqual([], self.parser._callbacks)
        self.parser.addDataCallback(callback)
        self.assertEqual([callback], self.parser._callbacks)

    def testCallCallback(self):
        self.parser.addDataCallback(callback)
        self.parser.parse(self.input)
        self.assertEqual([('ST', '12.34', 'g')], result)

    def testMultipleCalls(self):
        self.parser.addDataCallback(callback)
        self.parser.parse(self.input)
        self.assertEqual([('ST', '12.34', 'g')], result)
        self.parser.parse('ST 12.35 g')
        self.assertEqual([('ST', '12.35', 'g')], result)

#    def testBufferClearing(self):
#        self.parser.addDataCallback(callback)
#        self.parser.parse('nonsense')
#        self.parser.parse(self.input)
#        self.parser.parse('nonsense')
#        self.parser.parse(self.input)
#        self.assertEqual([('ST', '12.34', 'g'), ('ST', '12.34', 'g')], result)

if '__main__' == __name__:
    unittest.main()
