import unittest
import grpc
import sys
sys.path.append('../..')
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc

STOCKNAME_PRESENT = 'stock1'
STOCKNAME_NOT_PRESENT = 'IAmNotAStock'
HOSTNAME = 'localhost'
PORT='26119'
QUANTITY = 10
LARGE_QUANTITY = 100000000

def lookup(stockname):
    '''
    Function to initiate lookup on a stock
    :param stockname: name of the stock to initiate lookup on
    '''
    print(f"Sending lookup request for : {stockname}")
    
    #call catalog service
    hostAddr = HOSTNAME + ':' + PORT
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.CatalogServiceStub(channel)
        response = stub.Lookup(stocktrade_pb2.LookupRequest(stockname= stockname))
        print(
            f"Lookup request: {response.stockname}, response: Price of stock: {response.price}, Volume of the stock: {response.volume}")
        return response

def update(stockname, quantity, trade_type):
    '''
    Function to initiate sell/buy on a stock
    :param stockname: name of the stock to initiate trade on
    :param quantity: quantity being traded
    :param trade_type: type of the trade. BUY or SELL
    '''
    print(f"Sending update request of type: {trade_type} for : {stockname} with quantity: {quantity}")
    #call order service
    hostAddr = HOSTNAME + ':' + PORT
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.CatalogServiceStub(channel)
        response = stub.Update(stocktrade_pb2.UpdateRequest(
            stockname=stockname, quantity=quantity, trade_type=trade_type))
        print(
            f"Trade request: {stockname}, {quantity}, response status : {response.status}")
        return response

class TestCatalogService(unittest.TestCase):
    def test_lookup_basic(self):
        '''
        Function to test lookup on a stock
        '''
        print(f"Test lookup on a stock that is present in the database")
        lookup_response = lookup(STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response != None)
        self.assertTrue(lookup_response.stockname == STOCKNAME_PRESENT)
        self.assertTrue(lookup_response.price != None and lookup_response.price > 0)
        self.assertTrue(lookup_response.volume != None and lookup_response.volume >= 0)

    def test_update_sell(self):
        '''
        Function to test sell update on a stock
        '''
        print(f"Test sell update on a stock that is present in the database")
        #prevalidation tests
        lookup_response_before = lookup(STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response_before != None)
        self.assertTrue(lookup_response_before.stockname == STOCKNAME_PRESENT )
        self.assertTrue(lookup_response_before.price != None and lookup_response_before.price > 0)
        self.assertTrue(lookup_response_before.volume != None and lookup_response_before.volume >=0)

        #update validation
        update_response = update(STOCKNAME_PRESENT, QUANTITY, stocktrade_pb2.SELL)
        self.assertTrue(update_response != None)
        self.assertTrue(update_response.stockname == STOCKNAME_PRESENT)
        self.assertTrue(update_response.status != None and update_response.status == 1)

        #post validation tests
        lookup_response_after = lookup(STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response_after != None)
        self.assertTrue(lookup_response_after.stockname == STOCKNAME_PRESENT )
        self.assertTrue(lookup_response_after.price != None and lookup_response_after.price > 0)
        self.assertTrue(lookup_response_after.volume != None and lookup_response_after.volume >=0)
        self.assertTrue(lookup_response_after.price == lookup_response_before.price)
        self.assertTrue(lookup_response_after.volume) == lookup_response_before.volume + QUANTITY 

    def test_update_buy(self):
        '''
        Function to buy update on a stock
        '''
        print(f"Test buy update on a stock that is present in the database")
        #prevalidation tests
        lookup_response_before = lookup(STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response_before != None)
        self.assertTrue(lookup_response_before.stockname == STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response_before.price != None and lookup_response_before.price > 0)
        self.assertTrue(lookup_response_before.volume != None and lookup_response_before.volume >= 0)

        #update validation
        update_response = update(STOCKNAME_PRESENT, QUANTITY, stocktrade_pb2.BUY)
        self.assertTrue(update_response != None)
        self.assertTrue(update_response.stockname == STOCKNAME_PRESENT)
        self.assertTrue(update_response.status != None and update_response.status == 1)

        #post validation tests
        lookup_response_after = lookup(STOCKNAME_PRESENT) 
        self.assertTrue(lookup_response_after != None)
        self.assertTrue(lookup_response_after.stockname == STOCKNAME_PRESENT )
        self.assertTrue(lookup_response_after.price != None and lookup_response_after.price > 0)
        self.assertTrue(lookup_response_after.volume != None and lookup_response_after.volume >= 0)
        self.assertTrue(lookup_response_after.price == lookup_response_before.price)
        self.assertTrue(lookup_response_after.volume == lookup_response_before.volume - QUANTITY )

    def test_lookup_stock_not_found(self):
        '''
        Function to test lookup on a stock when stock is not present
        '''
        print(f"Test lookup on a stock that is not present in the database")
        lookup_response = lookup(STOCKNAME_NOT_PRESENT) 
        self.assertTrue(lookup_response != None)
        self.assertTrue(lookup_response.stockname == STOCKNAME_NOT_PRESENT)
        self.assertTrue(lookup_response.price != None and lookup_response.price == -1)
        self.assertTrue(lookup_response.volume != None and lookup_response.volume == -1)

    def test_update_stock_not_found(self):
        '''
        Function to test update on a stock when stock is not present
        '''
        print(f"Test update on a stock that is not present in the database")
        update_response = update(STOCKNAME_NOT_PRESENT, QUANTITY, stocktrade_pb2.BUY)
        self.assertTrue(update_response != None)
        self.assertTrue(update_response.stockname == STOCKNAME_NOT_PRESENT)
        self.assertTrue(update_response.status != None and update_response.status == -1)
    
    def test_update_stock_insufficient_volume(self):
        '''
        Function to test update on a stock when stock volume is insufficient for buy
        '''
        print(f"Test lookup on a stock that is present in the database but has insufficient volume for buy")
        update_response = update(STOCKNAME_PRESENT, LARGE_QUANTITY, stocktrade_pb2.BUY)
        self.assertTrue(update_response != None)
        self.assertTrue(update_response.stockname == STOCKNAME_PRESENT)
        self.assertTrue(update_response.status != None and update_response.status == 0)


if __name__ == '__main__':
    unittest.main()
