"""
    Server side code
"""

import socket
import config
import threading
import time
import logging
import thread_pool
import decimal
from model import stock

# stocks database 
stocks_db={}

def Lookup(name, stocks):
    """ 
    Checks if the stock is present in the stocks database

    :param name: name of the stock to be searched
    :param stocks: stocks database (dictionary)
    :returns:   the price of a meme stock if stock is present and is trading
                -1 if the company name is not found
                0 if the name is found and the stock trading is suspended

    """
    # time.sleep(8)
    try:
        if name in stocks:
            stock = stocks[name]
            print(f"{name} exists, isTrading: {stock.isTradable}")
            price = str(decimal.Decimal(str(stock.price)).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)) if stock.isTradable else str(0)
            return price
        else:
            print(f"{name} doesn't exist")
            return str(-1)
    except Exception as e:
        print(f"failed with exception: {e}")
        return str(-1)


def socketCommunication(tsocket, addr, args):
    """
    Function to communicate with client socket 

    :param tsocket: server side socket that is communicating with the client
    :param addr: client address
    :param args: contains the function called by client and its arguments in the form of a tuple

    """
    # print(threading.current_thread().name)
    message = f"connection initiated - message from server".encode()
    tsocket.send(message)

    func = args[0]
    database = args[1]
    stockname = tsocket.recv(1024).decode()
    stockPrice = func(stockname, database)
    threadname = threading.current_thread().name
    print(f"request from client: {stockname}, server response: {stockPrice}, on thread: {threadname}")
    tsocket.send(stockPrice.encode())
    # time.sleep(10)
    tsocket.close()  # Close the connection



def init_stocks_db():
    """
    Initializes stock database with name, price and maximum trading volume

    """
    print("initializing stocks database")
    gamestart_stock = stock.Stock("GameStart", config.gamestart_price)
    gamestart_stock.maxVolume = config.gamestart_max_vloume
    fishco_stock = stock.Stock("FishCo", config.fishco_price)
    fishco_stock.maxVolume = config.fishco_max_volume
    global stocks_db
    stocks_db = {gamestart_stock.name: gamestart_stock, fishco_stock.name: fishco_stock}


def serve():
    """
    Server creates a socket and starts to listen for incoming requests
    
    """
    sock = socket.socket()
    host = config.host
    port = config.port
    sock.bind((host, port))
    sock.listen(10)

    # thread pool object creation
    threadPoolObj = thread_pool.MyThreadPool(pool_size=config.thread_pool_size)

    while True:
        tsocket, addr = sock.accept()
        print(f"Connection from client:{addr} to server:{host} has been established.")
        
        # adding incoming requests to thread pool
        threadPoolObj.addReq(tsocket, addr, target=socketCommunication, args=(Lookup,stocks_db,) )
        
    threadPoolObj.endThreads()

if __name__ == '__main__':
    logging.basicConfig()
    init_stocks_db()
    serve()
    