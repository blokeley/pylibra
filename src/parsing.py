from __future__ import with_statement
import re
import threading
import logging

class Parser:
    """Stores incoming data in a buffer and parses it 
    using a regular expression."""
    
    def __init__(self, regex, callback = None):
        self.__dataLock = threading.RLock()
        self.__listenerLock = threading.RLock()
        self.__regex =  regex
        
        if not callback:
            self.__listeners = []
        else:
            self.__listeners = [callback]
        
        self.__data = ''
                
    def addListener(self, callback):
        "Adds the callback to be called when data is available."
        with self.__listenerLock:
            self.__listeners.append(callback)
        
    def removeListener(self, callback):
        with self.__listenerLock:
            self.__listeners.remove(callback)
            
    def __fireDataEvent(self):
        with self.__listenerLock:
            with self.__dataLock:
                if self.__listeners == []:
                    logging.warning("No callbacks listening for data.")
                    return
                for callback in self.__listeners:
                    callback()
        
    def parse(self, text):
        "Adds text to buffer, parses it and calls callbacks."
        with self.__dataLock:
            self.__data += text
        # Use the regex to search for data
        
        
    def __str__(self):
        "Returns a string representation of the parser."
        with self.__listenerLock:
            with self.__dataLock:
                return 'Data: {0}, Callbacks{1}'.format(self.__data, self.__listeners)
            