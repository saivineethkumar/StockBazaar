"""
    Client side code
"""

import socket
import config
import threading
import logging
import time
from tests import testUtil


def socketComm(stockname):
    """
    Code to run on each thread

    """

    # Creating socket and making connection with the server
    sock = socket.socket()
    host = config.host
    port = config.port
    sock.connect((host, port))
    print(f"Message received from server({host}:{port}) : {sock.recv(1024)}")

    # sending stock name and receiving the lookup status of that stock on the server
    print(f"calling lookup for {stockname}")
    sock.send(stockname.encode())
    fromserver = sock.recv(1024).decode()
    print(f"lookup response for {stockname}: {fromserver}")
    sock.close()


def testingSequentialCalls(stocks):
    """
    Making requests sequentially

    """
    for i in range(len(stocks)):
        socketComm(stocks[i])
       

def testingConcurrentCalls(stocks):
    """
    Making requests concurrently

    """
    threads = []
    for j in range(len(stocks)):
        thread = threading.Thread(target=socketComm, args=(stocks[j],))
        threads.append(thread)
        thread.start()
    
    for i in range(len(threads)):
        threads[i].join()
    

if __name__ == '__main__':
    logging.basicConfig()
    stocks = ["FishCo", "GameStart", "BoarCo", "MenhirCo","GameStart"]
    testingSequentialCalls(stocks)
    # testingConcurrentCalls(stocks)
    # testUtil.lookUpLatency(1000, socketComm, "GameStart")