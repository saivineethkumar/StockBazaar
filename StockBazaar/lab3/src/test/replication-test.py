import unittest
import grpc
import random
import sys
sys.path.append('../..')
from src import config
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc

HOSTNAME = config.order_hostname
PORTS = config.order_ports
QUANTITY = 10
LARGE_QUANTITY = 100000000
NUM_REQUESTS = 20
order_localdb = {}


def order(hostAddr, stockname, quantity, trade_type):
    '''
    Function to initiate trade on a stock
    :param hostAddr: host address of the service
    :param stockname: name of the stock to initiate trade on
    :param quantity: quantity being traded
    :param trade_type: type of the trade. BUY or SELL
    '''

    print(f"Sending trade request of type: {trade_type} for : {stockname} with quantity: {quantity}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
        order_response = stub.Trade(stocktrade_pb2.TradeRequest(stockname=stockname, quantity=quantity, trade_type=trade_type))
        print(f"Trade request: {stockname}, {quantity}, response status : {order_response.status}")
        return order_response
    

def order_lookup(hostAddr, order_id):
    '''
    Function to lookup an order id on a service
    :param hostAddr: host address of the service
    :param order_id: order id to be looked up
    '''

    print(f"Sending order lookup request for id: {order_id} at host: {hostAddr}")
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
        order_lookup_response = stub.OrderLookup(stocktrade_pb2.OrderLookupRequest(order_id= order_id))
        print(f"Order lookup request: {order_id}, response status : {order_lookup_response.status}")
        return order_lookup_response

'''
To test this file, we need to make sure that multiple order services are running and that the catalog service is running.
If the services are not running we cannot check this feature.
'''
class TestReplication(unittest.TestCase):
    def test_replication(self):
        '''
        Function to test whether replication is occuring fine or not
        '''

        # sending trade requests to the highest port number service assuming it is the leader
        hostAddr = HOSTNAME + ':' + str(PORTS[-1])
        for _ in range(NUM_REQUESTS):
            stockname = random.choice(stocks)
            trade_type = random.choice(['BUY', 'SELL'])
            quantity = random.choice(list(range(1,config.max_order_quantity)))
            order_response = order(hostAddr, stockname, quantity, trade_type)
            if order_response != None and order_response.status != None and order_response.status == 1:
                order_localdb[order_response.transaction_number] = (stockname, trade_type, quantity)
        
        # Send the locally stored order ids to all of the services to compare the data.
        # The data should be same everywhere
        for id, order_content in order_localdb.items():
            for port in PORTS:
                hostAddr = HOSTNAME + ':' + str(port)
                order_lookup_response = order_lookup(hostAddr, id)
                # status should be 1 meaning the order id exists
                self.assertTrue(order_lookup_response.status == 1)
                trade_type_resp = 'SELL' if order_lookup_response.trade_type == 1 else 'BUY'
                # once the status is 1, we check for the stock details corresponding to that order id
                self.assertTrue(order_content == (order_lookup_response.stockname, trade_type_resp, order_lookup_response.quantity))


if __name__ == '__main__':
    #test order request
    
    # creating stocknames to choose from to test working
    # some of the stocks are valid and present in stocksDB, some are not present - covering all cases
    global stocks
    stocks = ['stock'+str(i) for i in range(1,20)]
    
    unittest.main()
