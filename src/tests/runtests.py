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

"""Runs all test cases in current directory."""

import logging
import os
import re
import unittest

def get_tests(directory='.'):
    'Returns a test suite containing all of the tests in the given directory.'
    files = os.listdir(directory)
    tests = re.compile("^test.*py$")
    files = filter(tests.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)
    loader = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(loader, modules))

if __name__ == "__main__":
    logging.basicConfig()
    unittest.main(defaultTest='get_tests')
