#!/usr/bin/python
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
# along with pylibra. If not, see http://www.gnu.org/licenses/

"""Script to create Windows executable.

Example:
>>>python setup.py py2exe

"""

from distutils.core import setup
import os
import py2exe
import shutil
import zipfile

import core

README = os.path.abspath(r'../doc/README.html')
ICON = os.path.abspath(r'resources/dot.ico')

data_files = [
    ['',            ['libra.cfg', 'logging.cfg', README,]],
    ['resources',   [ICON,]],
]

# Create the executable
setup(
    version = core.__version__,
    description = 'pylibra serial data reader',
    name ='pylibragui',
    author = 'Tom Oakley',
    options = {
        'py2exe': {
            'bundle_files': 1,
            'dll_excludes': 'MSVCP90.dll',
            'compressed': 1,
        },
    },
    windows = ['pylibragui.py',],
    zipfile = None,
    data_files = data_files,
)

# Create the ZIP file to export
os.chdir('dist')
zfilename = 'pylibragui-%s-win32.zip' % core.__version__
zfile = zipfile.ZipFile(zfilename, 'w', zipfile.ZIP_DEFLATED)

# Add the executable to be distributed
data_files[0][1].insert(0, 'pylibragui.exe')

for group in data_files:
    for fname in group[1]:
        relative_path = os.path.relpath(
                            os.path.join(group[0],os.path.basename(fname))
                            )
        zfile.write(fname, relative_path)
zfile.close()

# Clean up
os.chdir(os.pardir)
shutil.rmtree('build')
