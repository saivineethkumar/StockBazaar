import unittest
import grpc
import sys
sys.path.append('../..')
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc

STOCKNAME = 'stock1'
STOCKNAME_NOT_PRESENT = 'IAmNotAStock'
HOSTNAME = 'localhost'
PORT='26117'
QUANTITY = 10
LARGE_QUANTITY = 100000000


def order(stockname, quantity, trade_type):
    '''
    Function to initiate trade on a stock
    :param stockname: name of the stock to initiate trade on
    :param quantity: quantity being traded
    :param trade_type: type of the trade. BUY or SELL
    '''
    hostAddr = HOSTNAME + ':' + PORT
    print(f"Sending trade request of type: {trade_type} for : {stockname} with quantity: {quantity}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
        order_response = stub.Trade(stocktrade_pb2.TradeRequest(stockname=stockname, quantity=quantity, trade_type=trade_type))
        print(f"Trade request: {stockname}, {quantity}, response status : {order_response.status}")
        return order_response

class TestOrderService(unittest.TestCase):
    def test_order(self):
        '''
        Function to test order on a stock
        '''
        #test buy
        print(f"Test buy order on a stock that is present in the database")
        order_response_buy = order(STOCKNAME, QUANTITY, stocktrade_pb2.BUY)
        order_response_buy != None
        self.assertTrue(order_response_buy.stockname == STOCKNAME)
        self.assertTrue(order_response_buy.status != None and order_response_buy.status == 1)
        self.assertTrue(order_response_buy.transaction_number != None and order_response_buy.transaction_number > 0)

        # test sell
        print(f"Test sell order on a stock that is present in the database")
        order_response_sell = order(STOCKNAME, QUANTITY, stocktrade_pb2.SELL)
        self.assertTrue(order_response_sell != None)
        self.assertTrue(order_response_sell.stockname == STOCKNAME)
        self.assertTrue(order_response_sell.status != None and order_response_sell.status == 1)
        self.assertTrue(order_response_sell.transaction_number != None and order_response_sell.transaction_number > 0)
    
    def test_order_stock_not_present(self):
        '''
        Function to test order on a stock that is not present
        '''
        #test buy
        print(f"Test buy order on a stock that is not present in the database")
        order_response_buy = order(STOCKNAME_NOT_PRESENT, QUANTITY, stocktrade_pb2.BUY)
        order_response_buy != None
        self.assertTrue(order_response_buy.stockname == STOCKNAME_NOT_PRESENT)
        self.assertTrue(order_response_buy.status != None and order_response_buy.status == -1)
        self.assertTrue(order_response_buy.transaction_number != None and order_response_buy.transaction_number == -1)

        # test sell
        print(f"Test sell order on a stock that is present in the database")
        order_response_sell = order(STOCKNAME_NOT_PRESENT, QUANTITY, stocktrade_pb2.SELL)
        self.assertTrue(order_response_sell != None)
        self.assertTrue(order_response_sell.stockname == STOCKNAME_NOT_PRESENT)
        self.assertTrue(order_response_sell.status != None and order_response_sell.status == -1)
        self.assertTrue(order_response_sell.transaction_number != None and order_response_sell.transaction_number == -1)
    
    def test_order_insufficient_volume(self):
        '''
        Function to test order on a stock that insufficient volume
        '''
        #test buy
        print(f"Test buy order on a stock that is present in the database but has insufficient volume")
        order_response_buy = order(STOCKNAME, LARGE_QUANTITY, stocktrade_pb2.BUY)
        order_response_buy != None
        self.assertTrue(order_response_buy.stockname == STOCKNAME)
        self.assertTrue(order_response_buy.status != None and order_response_buy.status == 0)
        self.assertTrue(order_response_buy.transaction_number != None and order_response_buy.transaction_number == -1)


if __name__ == '__main__':
    #test order request
    unittest.main()
