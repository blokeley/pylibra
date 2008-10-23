from __future__ import with_statement
import re
import threading
import logging

class AbstractParser:
    "Base class of parsers. Should not be initialized itself."
    
    def __init__(self):
        self.__observers = []
    
    def addListener(self, callback):
        if callback:
            self.__observers.append(callback)
            
    def removeListener(self, callback):
        if callback:
            self.__observers.remove(callback)
    
    def __fireDataEvent(self):
        if self.__listeners == []:
            logging.warning("No callbacks listening for data.")
            return
        for callback in self.__listeners:
            callback()
            
    def parse(self, data):
        msg = 'parse() must be overridden by subclasses'
        raise NotImplementedError(msg)
                    
class Parser(AbstractParser):
    """Stores incoming data in a buffer and parses it 
    using a regular expression."""
    
    def __init__(self, regex, callback = None):
        self.__regex =  regex
        self.__data = ''
                
    def parse(self, text):
        "Adds text to buffer, parses it and calls callbacks."
        self.__data += text
        # Use the regex to search for data
        
    def __str__(self):
        "Returns a string representation of the parser."
        return 'Data: {0}, Callbacks{1}'.format(self.__data, self.__listeners)
            
class DummyParser(AbstractParser):
    "Creates dummy serial events"
    
    def __init__(self):
        self.__count = 0
    
    def parse(self):
        for callback in self.__observers:
            callback([count, count + 1])
    
    def __str__(self):
        return 'Callbacks: {0}, Count: {1}'.format(self.__observers, self.__count)
    