"""
Custom Thread Pool implementation
"""

import threading
import time
from threading import Lock

class MyThreadPool:
    """
    Attributes:
    -----------
    _pool_size: thread pool size, taken as an input from the config file
    _reqQ: request queue - to maintain all the incoming requests to the thread pool
    _lock: mutex lock to prevent race conditions
    _threads: list of all the threads in the thread pool

    """
    def __init__(self, pool_size):
        """
        Constructor
        :param pool_size: thread pool size 

        """
        self._pool_size = pool_size
        self._reqQ = []
        self._lock = Lock()
        self._threads = []
        for i in range(pool_size):
            thread = threading.Thread(target=self._threadedFunction)
            thread.name = str(i)
            self._threads.append(thread)
            thread.start()

    def _getSocketFromQueue(self):
        """
        Returns queue element based on lock acquire and release
        :returns: tuple of socket, target function, and its arguments

        """
        self._lock.acquire()
        if len(self._reqQ) != 0:
            tsocket, addr, target, args = self._reqQ[0]
            self._reqQ.pop(0)
            self._lock.release()
            return (tsocket, addr, target, args)
        else:
            self._lock.release()
            return (None,None,None,None)

    def _threadedFunction(self):
        """
        Code to run on each thread

        """
        while True:
            try :
                tsocket, addr, target, args = self._getSocketFromQueue()
                if tsocket is not None:
                    target(tsocket, addr, args)
            except Exception as e:
                print(f"Thread failed with an Exception: {e}")


    def addReq(self, socket, addr, target, args):
        """
        Adding request to the thread pool
        :param socket: socket on which communication is established
        :param addr: address of the client
        :param target: target function that client called
        :param args: arguements to the above target function
        
        """
        with self._lock:
            self._reqQ.append((socket, addr, target, args))


    def endThreads(self):
        """
        calls .join() method on all the threads. 
        Thread pool will stop once all the threads are done with their tasks

        """
        for i in range (self._pool_size):
            self._threads[i].join()
    
