#!/usr/bin/env python
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
# along with pylibra.  If not, see http://www.gnu.org/licenses/

"""Unit tests for the parsing module."""

import logging
import unittest

import runtests
# Add parent directory to python path
runtests.append_src_path()

import parsing


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
        """Overrides `TestCase.setUp()`."""
        self.regex = r'(ST|OL)\s*(\d+\.\d+)\s*(\S?)'
        self.parser = parsing.RegexParser(self.regex)
        self.input = 'x ST 12.34 g x'
    
    def tearDown(self):
        """Overrides `TestCase.tearDown()`."""
        self.parser = None
        result = None
    
    def test_initial_callback(self):
        self.parser = parsing.RegexParser(self.regex, callback)
        self.assertTrue([callback], self.parser._callbacks)
        
    def test_add_callback(self):
        self.assertEqual([], self.parser._callbacks)
        self.parser.add_data_callback(callback)
        self.assertEqual([callback], self.parser._callbacks)

    def test_call_callback(self):
        self.parser.add_data_callback(callback)
        self.parser.parse(self.input)
        self.assertEqual([('ST', '12.34', 'g')], result)

    def test_multiple_calls(self):
        self.parser.add_data_callback(callback)
        self.parser.parse(self.input)
        self.assertEqual([('ST', '12.34', 'g')], result)
        self.parser.parse('ST 12.35 g')
        self.assertEqual([('ST', '12.35', 'g')], result)
    
    def test_single_parsing(self):
        for input, output in REGEXTESTS:
            self.p = parsing.RegexParser(OXFORDREGEX)
            self.assertEqual(output, self.p.parse(input))

    def test_multiple_parsing(self):
        self.p = parsing.RegexParser(OXFORDREGEX)

        for input, output in REGEXTESTS:
            self.assertEqual(output, self.p.parse(input))

class TestWordParser(unittest.TestCase):
    
    def test_single_parsing(self):
        for input, output in WORDTESTS:
            self.p = parsing.WordParser()
            self.assertEqual(output, self.p.parse(input))

    def test_multiple_parsing(self):
        self.p = parsing.WordParser()
        
        for input, output in WORDTESTS:
            self.assertEqual(output, self.p.parse(input))
   
if '__main__' == __name__:
    logging.basicConfig()
    unittest.main()
