import logging

import grpc
import stocktrade_pb2
import stocktrade_pb2_grpc
import config
import threading
from test import testutil


def lookup(stockname):
    '''
    Function to initiate lookup on a stock
    :param stockname: name of the stock to initiate lookup on
    '''
    hostAddr = config.host + ':' + str(config.port)
    print(f"Sending lookup request for : {stockname}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.StockTradeStub(channel)
        response = stub.Lookup(stocktrade_pb2.StockName(name=stockname))
        print(
            f"Lookup request: {stockname}, response: Price of stock: {response.price}, Volume of the stock: {response.volume}")


def trade(stockname, quantity, trade_type):
    '''
    Function to initiate trade on a stock
    :param stockname: name of the stock to initiate trade on
    :param quantity: quantity being traded
    :param trade_type: type of the trade. BUY or SELL
    '''
    hostAddr = config.host + ':' + str(config.port)
    print(
        f"Sending trade request of type: {trade_type} for : {stockname} with quantity: {quantity}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.StockTradeStub(channel)
        response = stub.Trade(stocktrade_pb2.TradeInput(
            name=stockname, quantity=quantity, type=trade_type))
        print(
            f"Trade request: {stockname}, {quantity}, response status : {response.trade_status}")


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
    # testutil.testLookupFunctionsSeq(1000)
    # testutil.testTradeFunctionsSeq(1000)
    # testutil.testupdateFunctionsSeq(1000)

    # use this function to make requests sequentially
    testutil.testAllFunctionsSeq()

    # use this function to make requerts concurrently
    # pass the deisred number of loop runs as paramater
    testutil.testAllFunctionsConcurrently(100)
