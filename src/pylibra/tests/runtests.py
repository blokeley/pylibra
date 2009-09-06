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
import sys
import time
import unittest

def get_tests(directory=os.curdir):
    """Return a test suite containing all of the tests in the given directory."""
    files = os.listdir(directory)
    pattern = re.compile("^test.*py$")
    moduleNames = [os.path.splitext(file_)[0] for file_ in files if pattern.search(file_)]
    modules = [__import__(mod) for mod in moduleNames]
    loader = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(loader(mod) for mod in modules)

def setup_logging():
    """Configure loggers without need for a config file."""
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='%s-tests.log' % time.strftime('%Y-%m-%d_%H-%M-%S'),
                    filemode='w')

def append_src_path():
    """Append the directory of source files to sys.path."""
    src_path = os.path.dirname(os.getcwd())
    if not src_path in sys.path:
        sys.path.append(src_path)


if __name__ == "__main__":
    setup_logging()
    unittest.main(defaultTest='get_tests')
