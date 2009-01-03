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

# Maximum length of any text buffer
_MAXBUFFERSIZE = 65536

class AbstractParser(object):
    'Base class of parsers. Should not be initialized itself.'
    
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
                    
class RegexParser(AbstractParser):
    'Stores incoming data in a buffer and parses it using a regular expression.'

    def __init__(self, regex, *callbacks):
        AbstractParser.__init__(self, *callbacks)
        self._pattern = re.compile(regex)
        self._buffer = ''
                
    def parse(self, data):
        '''Adds text to buffer, parses it and calls callbacks.
        
        @param data: a string of data to parse.
        @return: a list of lines, each line being a tuple of matched data.
        '''
        self._buffer += data
        # Use the regex to search for data
        results = self._pattern.findall(self._buffer)

        if results:
            # Remove the data from the buffer
            self._buffer = self._pattern.sub('', self._buffer)
            # Tell the callbacks about new data
            self._callDataCallbacks(results)
            
        # If the buffer is getting too long, slice off the first half
        if len(self._buffer) > _MAXBUFFERSIZE:
            self._buffer = self._buffer[(_MAXBUFFERSIZE/2):]
            
        return results
        
    def __str__(self):
        "Returns a string representation of the parser."
        return 'Data: %s, Callbacks: %s' % (self._data, self._callbacks)
 
class WordParser(AbstractParser):
    '''Stores incoming data in a buffer and returns 
    a list of lines. Each line is a tuple of words.
    '''
    
    def __init__(self, *callbacks):
        AbstractParser.__init__(self, *callbacks)
        self._linepattern = re.compile(r'.*')
        self._wordpattern = re.compile(r'\b(\S+)\b')
        self._buffer = ''
        
    def parse(self, data):
        '''Adds text to buffer, parses it and calls callbacks.

        @param data: a string of data to parse.
        @return: a list of lines, each line being a tuple of words.
        '''
        self._buffer += data
        results = []
        lastlineindex = 0
        lastwordindex = 0
        
        # Use finditer() rather than findall() so that 
        # the last index i.e. end() can be recorded.
        for line in self._linepattern.finditer(self._buffer):
            # Ignore empty line match objects
            if line:
                # Record the index of the last line match
                lastlineindex = line.end()
                words = []
                
                # Iterate through matched words in the line
                for word in self._wordpattern.finditer(line.group(0)):
                    # Ignore empty word match objects
                    if word:
                        # Record the index of the last word match
                        lastwordindex = word.end()
                        words.append(word.group(0))
                
                if words: results.append(tuple(words))
        
        # Remove data up to end of matches
        lastmatchindex = lastlineindex + lastwordindex
        self._buffer = self._buffer[lastmatchindex:]
        
        # If the buffer is getting too long, slice off the first half
        if len(self._buffer) > _MAXBUFFERSIZE:
            self._buffer = self._buffer[(_MAXBUFFERSIZE/2):]        
        
        if results: self._callDataCallbacks(results)
        return results
