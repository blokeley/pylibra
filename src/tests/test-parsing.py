#! /usr/bin/env python

import unittest
import logging
import parsing

def callback(arg):
    "Dummy method to return the argument."
    return arg

class TestParsing(unittest.TestCase):
    "Tests parsing classes and functions."
    
    def setUp(self):
        self.regex = '\\d.\\d'
        self.parser = parsing.Parser(self.regex)
    
    def tearDown(self):
        self.parser = None
    
    def testInitialCallback(self):
        self.parser = parsing.Parser(self.regex, callback)
        self.assertTrue([callback], self.parser._Parser__listeners)
        
    def testAddCallback(self):
        self.assertEqual([], self.parser._Parser__listeners)
        self.parser.addListener(callback)
        self.assertEqual([callback], self.parser._Parser__listeners)
        
if '__main__' == __name__:
    unittest.main()
