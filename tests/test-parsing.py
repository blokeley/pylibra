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

'Unit tests for the parsing module.'

import os
import sys
# Fiddle module loading path to get parsing module
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'pylibra'))
import parsing

import unittest

def callback(data):
    global result
    result = data

OXFORDREGEX = r'(ST)\s*([+-]?\d+\.?\d*)\s*(\S+)'

REGEXTESTS = (
        ('1', []),
        ('ST +12.34 g', [('ST', '+12.34', 'g')]),
        ('ST +12.34 g ST +12.34 g ', [('ST', '+12.34', 'g'), ('ST', '+12.34', 'g')]),
        ('ST -1 kg', [('ST', '-1', 'kg')])
        )

WORDTESTS =(
        ('some text', [('some', 'text')]),
        ('some text\n', [('some', 'text')]),
        ('some text1\nsome text2', [('some', 'text1'), ('some', 'text2')])
        )

class TestRegexParser(unittest.TestCase):
    
    def setUp(self):
        self.regex = r'(ST|OL)\s*(\d+\.\d+)\s*(\S?)'
        self.parser = parsing.RegexParser(self.regex)
        self.input = 'x ST 12.34 g x'
    
    def tearDown(self):
        self.parser = None
        result = None
    
    def testInitialCallback(self):
        self.parser = parsing.RegexParser(self.regex, callback)
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
    
    def testSingleParsing(self):
        for input, output in REGEXTESTS:
            self.p = parsing.RegexParser(OXFORDREGEX)
            self.assertEqual(output, self.p.parse(input))

    def testMultipleParsing(self):
        self.p = parsing.RegexParser(OXFORDREGEX)

        for input, output in REGEXTESTS:
            self.assertEqual(output, self.p.parse(input))

class TestWordParser(unittest.TestCase):
    
    def testSingleParsing(self):
        for input, output in WORDTESTS:
            self.p = parsing.WordParser()
            self.assertEqual(output, self.p.parse(input))

    def testMultipleParsing(self):
        self.p = parsing.WordParser()
        
        for input, output in WORDTESTS:
            self.assertEqual(output, self.p.parse(input))
   
if '__main__' == __name__:
    unittest.main()
