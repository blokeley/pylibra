#!/usr/bin/env python
"""Run all test cases."""

import functools
import logging
import os
import re
import sys
import time
import unittest


def setup_logging():
    """Configure loggers without need for a config file."""
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='%s-tests.log' % time.strftime('%Y-%m-%d_%H-%M-%S'),
                    filemode='w')


def todo(func):
    """Decorator that ignores exceptions raised by given unittest method.

    Use to annotate test methods for code that may not be written yet.
    If there are failures in the annotated test method ignore the failure; 
    if the test unexpectedly succeeds, raise an AssertionError.
    
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning('%s is marked "todo"' % func.__name__)
        try:
            func(*args, **kwargs)
            succeeded = True
        except:
            succeeded = False
        assert succeeded is False, "%s marked TODO but passed" % func.__name__
    return wrapper


def ignore(func):
    """Decorator that ignores the given function and logs a warning."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning('Ignoring %s' % func.__name__)
    return wrapper


def add_path(path=os.curdir):
    """Add the path to sys.path if it is not already present."""
    abspath = os.path.abspath(path)
    if abspath not in sys.path:
        sys.path.append(abspath)


def find_modules(path=os.curdir):
    """Find directories containing python source files and add them to sys.path"""
    pythonfile_pattern = re.compile(r'^.*\.py$')

    # Walk the directory tree looking for python source
    for root, dirs, files in os.walk(path):
        for filename in files:
            if pythonfile_pattern.search(filename):
                # File is python source: add its module to sys.path
                add_path(root)


def create_testsuite(names=None):
    """Return a `unittest.TestSuite` containing tests in names.

    If names is None, search the tree below the current directory for tests.
    For formats of names see `unittest.defaultTestLoader.loadTestsFromName()`

    """

    # Set up a test suite
    suite = unittest.TestSuite()

    # Set up the search regex for tests
    testfile_pattern = re.compile(r'^test.*\.py$')

    # If named tests or modules are given, add them to the suite
    if names:
        loader = unittest.defaultTestLoader.loadTestsFromNames
        suite.addTests(loader(names))

    else:
        # Walk the directory tree looking for tests
        loader = unittest.defaultTestLoader.loadTestsFromName
        for root, dirs, files in os.walk(os.curdir):
            for filename in files:
                if testfile_pattern.search(filename):
                    add_path(root)
                    # File is a test: add it to the test suite
                    suite.addTests(loader(os.path.splitext(filename)[0]))

    return suite


if __name__ == "__main__":
    setup_logging()

    # Add parent directory and sub directories to path
    add_path(os.pardir)
    find_modules()

    # Create a TestSuite and run it
    suite = create_testsuite(sys.argv[1:])
    unittest.TextTestRunner(verbosity=2).run(suite)
