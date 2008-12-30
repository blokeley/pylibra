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

import re
import logging

class AbstractParser(object):
    "Base class of parsers. Should not be initialized itself."
    
    def __init__(self, *callbacks):
        if callbacks:
            self._callbacks = list(callbacks)
        else:
            self._callbacks = []

        self._logger = logging.getLogger(__name__)
    
    def addDataCallback(self, callback):
        'Adds callback to list of functions to call.'
        if callback: self._callbacks.append(callback)
            
    def removeDataCallback(self, callback):
        'Removes callback from list of functions to call'
        if callback: self._callbacks.remove(callback)
    
    def _callDataCallbacks(self, results):
        if not self._callbacks:
            self._logger.warning("No callbacks listening for data.")
            return
        for callback in self._callbacks:
            callback(results)
            
    def parse(self, data):
        msg = 'parse() must be overridden by subclasses'
        raise NotImplementedError(msg)
                    
class Parser(AbstractParser):
    'Stores incoming data in a buffer and parses it using a regular expression.'

    MAXBUFFERSIZE = 10240

    def __init__(self, regex, *callbacks):
        AbstractParser.__init__(self, *callbacks)
        assert regex
        self._pattern = re.compile(regex)
        self._buffer = ''
                
    def parse(self, text):
        "Adds text to buffer, parses it and calls callbacks."
        self._buffer += text
        results = self._pattern.findall(self._buffer)

        if results:
            # Tell the callbacks about new data
            self._callDataCallbacks(results)
            # Remove the data from the buffer
            self._buffer = self._pattern.sub('', self._buffer)

        # If the buffer is getting too long, slice off the first half
        if len(self._buffer) > Parser.MAXBUFFERSIZE:
            self._buffer = self._buffer[(Parser.MAXBUFFERSIZE/2):]
        
    def __str__(self):
        "Returns a string representation of the parser."
        return 'Data: %s, Callbacks: %s' % (self._data, self._callbacks)
    