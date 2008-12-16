#! /usr/bin/python

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

'Test harness to check regular expressions.'

import re

def main():
    tests = [
    (r'hell', 'hello', 'hell'),
    (r'\d'  , '1'   , '1'),
    (r'\d\.\d', '1.2', '1.2'),
    (r'\d\.\d', 'xx1.2xx', '1.2'),
    (r'.*\d\.\d.*', 'xx1.2xx', '1.2'),
    (r'.*(\d\.\d).*', 'xx1.2xx', '1.2'),
    (r'.+(\d\.\d)+.+', 'xx1.2xx xx3.4xx', '1.2'),
    (r'ab', 'abab', 'abab'),
    (r'\d\.\d', 'xx1.2xx xx3.4xx', '1.2 3.4'),
    (r'\d+\.\d+', 'xx12.34xx', ''),
    (r'(ST|OL)\s*(\d+\.\d+)\s*(\S?)', 'ST 12.34 g', '')
    ]

    for regex, text, expected in tests:
        results = re.compile(regex).findall(text)
        if results:
            print 'regex: %-15s text: %-20s results: %-20s pass: %-15s' % \
            (regex, text, results, (results == expected))
        else:
            print 'regex: %-15s text: %-15s did not match' % (regex, text)

if __name__ == "__main__":
    main()
