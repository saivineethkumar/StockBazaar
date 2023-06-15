from concurrent import futures
import logging

import grpc
import stocktrade_pb2
import stocktrade_pb2_grpc
import threading
import config
from model import stock
import time
from threading import Lock

stocks_db = {}
lock = Lock()


class StockTrade(stocktrade_pb2_grpc.StockTradeServicer):

    def Lookup(self, request, context):
        ''' 
        Funtion to return the price and the trading volume of a stock
        :param  name:  The name of the stock to perform lookup on
        :return price: price of the stock if stock is found, -1 otherwise
        :return volume: volume traded so far of the stock if stock is found, -1 otherwise
        '''
        print("Lookup: ", request.name, " on ",
              threading.current_thread().name)
        try:

            name = request.name  # name of the stock to perform lookup on
            print(f'Received lookup request for : {name}')
            # if stock is present in database return price and volume from db
            if name in stocks_db:
                stock = stocks_db[name]
                return stocktrade_pb2.StockInfo(price=stock.getPrice(), volume=stock.volume)
            # if stock is not present in database return price and volume as -1
            return stocktrade_pb2.StockInfo(price=-1, volume=-1)
        except Exception as e:
            print(
                f"Failed to process lookup request for request : {request} with exception: {e}")
            return stocktrade_pb2.StockInfo(price=-1, volume=-1)

    def Trade(self, request, context):
        '''
        Function to perform trading on a stock
        :param name: the name of the stock
        :param quantity: the volume traded
        :param type: type of the trade. Either BUY or SELL
        :return trade_status: 1 if trading is succesfull, 0 if trading is suspended, -1 otherwise
        '''
        print("Trade: ", request.name, " on ", threading.current_thread().name)
        try:
            # time.sleep(5)
            name = request.name  # name of the stock that is being traded
            quantity = request.quantity  # quantity being traded
            type = request.type  # type of trade (BUY or SELL)
            print(
                f'Received trade request with quantity: {quantity} of type: {type} for : {name}')
            if name in stocks_db:
                with lock:
                    stock = stocks_db[name]
                    # call the trade function on stock to perform trading
                    trade_status = stock.trade(quantity=quantity, type=type)

                # return trade_status 1 if trade is successfull and 0 otherwise
                return stocktrade_pb2.TradeStatus(trade_status=1 if trade_status else 0)

        except Exception as e:
            print(
                f"Failed to process trade request for request : {request} with exception: {e}")
        # return trade_status -1 if stock is invalid or the function fails
        return stocktrade_pb2.TradeStatus(trade_status=-1)

    def Update(self, request, context):
        '''
        Function to update the price of a stock.
        :param name: The name of the stock to update.
        :param price: The price to update to.
        :return: 1 if the update is successful, otherwise 0.
        '''
        print("Update: ", request.name, " on ",
              threading.current_thread().name)
        try:
            # time.sleep(5)
            name = request.name  # name of the stock
            price = request.price  # new price of the stock
            print(
                f'Received update request for : {name} with new price {price}')
            if name in stocks_db:
                with lock:
                    stock = stocks_db[name]
                    # call the update function on stock to perform update
                    update_status = stock.updatePrice(price=price)
                # return update_status 1 if update is succesfull, -2 otherwise
                return stocktrade_pb2.UpdateStatus(update_status=1 if update_status else -2)
            return stocktrade_pb2.UpdateStatus(update_status=-1)
        except Exception as e:
            print(
                f"Failed to process update request for request : {request} with exception: {e}")
        # return update_status -1 if stock is invalid or the function fails
        return stocktrade_pb2.UpdateStatus(update_status=-1)


def serve(hostAddr):
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=config.thread_pool_size))
    stocktrade_pb2_grpc.add_StockTradeServicer_to_server(StockTrade(), server)
    # to connect between 2 machines, keep the server hostname here eg: "elnux3.cs.umass.edu:50051"
    server.add_insecure_port(hostAddr)
    server.start()
    server.wait_for_termination()


def init_stocks_db():
    '''
    Function to initilize in-memory database
    adds the stocks [GameStart, FishCo, BoarCo, Menhir] to the db
    '''
    print("initializing stocks database")
    # create stock objects with starting price and max volume
    gamestart_stock = stock.Stock("GameStart", config.gamestart_price)
    gamestart_stock.maxVolume = config.gamestart_max_vloume
    fishco_stock = stock.Stock("FishCo", config.fishco_price)
    fishco_stock.maxVolume = config.fishco_max_volume
    boarco_stock = stock.Stock("BoarCo", config.boarco_price)
    boarco_stock.maxVolume = config.boarco_max_volume
    menhirco_stock = stock.Stock("MenhirCo", config.menhirco_price)
    menhirco_stock.maxVolume = config.menhirco_max_volume
    # add the stock objects to db
    global stocks_db
    stocks_db = {gamestart_stock.name: gamestart_stock, fishco_stock.name: fishco_stock,
                 boarco_stock.name: boarco_stock, menhirco_stock.name: menhirco_stock}


if __name__ == '__main__':
    logging.basicConfig()
    # initialize database
    init_stocks_db()
    hostAddr = config.host + ':' + str(config.port)
    # start the server on hostAddr to receive requests
    serve(hostAddr)
