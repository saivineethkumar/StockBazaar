import logging
import grpc
import stocktrade_pb2
import stocktrade_pb2_grpc
import config
import random
import time


def update(stockname, trade_price):
    '''
    Function to initiate update on a stock
    :param stockname: name of the stock to initiate update on
    :param trade_price: new price of the stock
    '''
    hostAddr = config.host + ':' + str(config.port)
    print(
        f"Sending update request for : {stockname} with new price {trade_price}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.StockTradeStub(channel)
        response = stub.Update(stocktrade_pb2.UpdateInput(
            name=stockname, price=trade_price))
        print(
            f"Update request: {stockname}, {trade_price}, response status : {response.update_status}")


if __name__ == '__main__':
    logging.basicConfig()
    stocks = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo']
    while (True):
        # Generate a random price between 1 and 1000
        new_price = random.randint(1, 1000)

        # Generate a random stock
        stockName = stocks[random.randint(0, len(stocks)-1)]

        update(stockname=stockName, trade_price=new_price)

        # Wait for a random amount of time before the next update
        time.sleep(random.randint(1, 10))
