#! /usr/bin/python
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

'''Script to create Windows executable.

Example:
>>>python setup.py py2exe
'''

from distutils.core import setup
import os
import py2exe
import shutil

# Create the executable
setup(console=['textui.py'])

# Copy config files across
for file in ('libra.cfg', 'logging.cfg'):
    shutil.copy(file, 'dist')

# Clean up
shutil.rmtree('build')
