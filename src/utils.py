#! /usr/bin/env python

# Copyright 2008 Tom Oakley 
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylibra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pylibra.  If not, see <http://www.gnu.org/licenses/>.

"""Utility classes."""

import Queue
import threading

class PeriodicTimer(threading.Thread):
    """Periodically call a function.

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
        """Create a PeriodicTimer that will repeatedly call function with
        arguments args and keyword arguments kwargs, after interval
        seconds have passed.
        
        """
        threading.Thread.__init__(self)
        self.setDaemon(True) # Do not keep program running
        self.__interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.__finished = threading.Event()

    def end(self):
        """Make a best effort attempt to stop the PeriodicTimer.

        If the thread is currently executing the function, this effort
        may not immidiately succeed. The PeriodicTimer is then stopped
        when execution returns from the function. If the function
        never returns, the thread will not be stopped.
        
        """
        self.__finished.set()

    def run(self):
        while True:
            self.__finished.wait(self.__interval)
            if self.__finished.isSet():
                break
            self.function(*self.args, **self.kwargs)


class FlushFile(object):
    """Wrapper around any file that immediately flushes after write().
    
    Example:
    >>>import sys
    >>>sys.stdout = FlushFile(sys.stdout)
    >>>print 'hello' # Prints almost immediately
    
    """
    def __init__(self, f): self.f = f
        
    def write(self, msg):
        """Write msg to file almost immediately."""
        self.f.write(msg)
        self.f.flush()

    def flush(self):
        """Flush exposed for libraries such as logging that explicitly flush."""
        self.f.flush()


class Serializer(threading.Thread):
    """Serializes all calls to execute() on to 1 thread.

    See "Python in a Nutshell" 2nd ed., Alex Martelli,
    p285 for more information.
    
    """
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        self.__workRequestQueue = Queue.Queue()
        self.__resultQueue = Queue.Queue()
        self.__finished = threading.Event()
        self.start()

    def execute(self, callable, *args, **kwargs):
        """Called by other threads as callable would be."""
        self.__workRequestQueue.put((callable, args, kwargs))
        return self.__resultQueue.get()

    def end(self):
        """Make a best effort attempt to stop the Serializer.

        If the thread is currently executing the function, this effort
        may not immidiately succeed. The Serializer is then stopped
        when execution returns from the function. If the function
        never returns, the thread will not be stopped.
        
        """
        self.__finished.set()

    def run(self):
        while not self.__finished.isSet():
            callable, args, kwargs = self.__workRequestQueue.get()
            self.__resultQueue.put(callable(*args, **kwargs))
