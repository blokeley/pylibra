"Module for reading and writing data to and from a file."

from __future__ import with_statement
import csv
import logging

def save(data, filename='data.csv'):
    "Saves the data to the given filename"
    
    logging.debug('Saving %s' % filename)
    
    with open(filename, 'w') as outFile:
        writer = csv.writer(outFile)
        writer.writerows(data)
        
    logging.debug('Finished saving %s' % filename)
