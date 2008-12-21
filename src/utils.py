#! /usr/bin/env python

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

'Utility classes and functions.'

import logging
import threading

class PeriodicTimer(threading.Thread):
    """
    Periodically call a function.

    PeriodicTimers are, like threads, started by calling their start()
    method. An attempt to ending them can be made by calling their
    end() method.

    PeriodicTimers use fixed-delay execution which means that the
    delay between subsequent invokations of the function is
    fixed. Because the execution time of the function is not accounted
    for, the periods therefore become more and more distorted in
    relation to real time. That makes PeriodicTimers unsuitable for
    long running threads in which it is critical that each function
    call time is as accurate as possible.

    For example:

        def hello():
            print "Hi there!"

        t = PeriodicTimer(5, hello)
        t.start()    # "Hi there!" will be printed every five seconds.
        
    """
    def __init__(self, interval, function, *args, **kwargs):
        """
        Create a PeriodicTimer that will repeatedly call function with
        arguments args and keyword arguments kwargs, after interval
        seconds have passed.
        """
        threading.Thread.__init__(self)
        self.setDaemon(True) # Do not keep program running
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()
        self.__logger = logging.getLogger(__name__)

    def end(self):
        """
        Make a best effort attempt to stop the PeriodicTimer.

        If the thread is currently executing the function, this effort
        may not immidiately succeed. The PeriodicTimer is then stopped
        when execution returns from the function. If the function
        never returns, the thread will not be stopped.
        """
        self.finished.set()

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                break
            self.__logger.debug('Calling %s' % str(self.function))
            self.function(*self.args, **self.kwargs)

class FlushFile(object):
    """Wrapper around any file that immediately flushes after write().
    
    For example:
    
        import sys
        sys.stdout = FlushFile(sys.stdout)
        print 'hello' # Prints almost immediately
    """
    def __init__(self, f): self.f = f
        
    def write(self, msg):
        'Writes msg to file almost immediately'
        self.f.write(msg)
        self.f.flush()

    def flush(self):
        'Flush exposed for libraries such as logging that explicitly flush'
        self.f.flush()
