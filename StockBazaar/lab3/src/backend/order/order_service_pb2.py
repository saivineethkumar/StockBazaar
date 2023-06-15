import grpc
from threading import Lock
from queue import Queue

import sys
sys.path.append('../../..')
from src import config
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc
from src.shared.util import logging
from src.shared.model import order

stockorders_db = {}     # stock orders db to store all the stock trade requests
curr_tran = 0           # current transaction number to keep track of transactions
lock = Lock()           # lock to access the above global variables
updated_stocks_queue = Queue()             # queue to stream db updates
leader_id = 0           # leaderid elected by the frontend
logger = logging.logger('order-service-pb')
service_id = 0          # id of the current service

class OrderService(stocktrade_pb2_grpc.OrderServiceServicer):

    def Trade(self, request, context):
        ''' 
        Funtion to return the transaction status and transaction number for a requested trade order
        :param  request: contains the stockname, trade type (enum) and quantity
        :return response: contains the stockname, transaction status and number
        '''
        try:
            name = request.stockname
            type = request.trade_type
            quantity = request.quantity
            trade_type_word = 'SELL' if type == 1 else 'BUY'
            global service_id
            logger.info(f'Received Trade request for: {name},{trade_type_word},{quantity} on order-service_{service_id}')
    
            hostAddr = config.catalog_hostname + ':' + str(config.catalog_port)
            # sending the trade request to catalog for checking and updating the stockDB at catalog
            with grpc.insecure_channel(hostAddr) as channel:
                stub = stocktrade_pb2_grpc.CatalogServiceStub(channel)
                response = stub.Update(stocktrade_pb2.UpdateRequest(stockname=name, trade_type=type, quantity=quantity ))
                logger.info(f"Trade request: {name},{trade_type_word},{quantity}, response: status: {response.status}")
                global updated_stocks_queue
                updated_stocks_queue.put(name)
                # if trade is processed correctly, increase the transaction number and save it to in-memory stockorders_db
                if response.status == 1:
                    with lock:
                        # TODO : write lock
                        global curr_tran
                        global stockorders_db
                        curr_tran = curr_tran + 1
                        stockorders_db[curr_tran] = order.Order(order_id=curr_tran, stockname=name, trade_type=trade_type_word, quantity=quantity)
                        self.write_order_to_file()
                        # TODO: can run replicate_order on seperate thread instead of sequentially
                        self.replicate_order(curr_tran, name, type, quantity)
                        return stocktrade_pb2.TradeResponse(stockname=name,status=response.status, transaction_number=curr_tran)
                # if trade is not processed, return status with transaction number -1 to indicate failure.
                return stocktrade_pb2.TradeResponse(stockname=name,status=response.status, transaction_number=-1)
        except Exception as e:
            logger.error(f"Failed to process Trade request in order-service_{service_id} for request : {request}. Failed with exception: {e}")
        return stocktrade_pb2.TradeResponse(stockname=name,status=-1, transaction_number=-1)

    def OrderLookup(self, request, context):
        ''' 
        Funtion to query am existing order. Returns the order id, stockname, type, and quantity of the order
        :param  request:  contains the id of the order to perform lookup on
        :return response: contains the order id, name, type and quantity traded in the order.
        status field is also added in the response. If the order is found, status is set to 1, otherwise -1.
        '''
        try:
            global service_id
            order_id = int(request.order_id)  # id of the order to perform lookup on
            logger.info(f'Received lookup request for order: {order_id} on order service {service_id}')
            # if the order is present in database return name, type, and quantity from db
            global stockorders_db
            if order_id in stockorders_db:
                with lock:
                    # TODO: read lock
                    order_info = stockorders_db[order_id]
                    trade_type_enum = 1 if order_info.trade_type=='SELL' else 0 if order_info.trade_type=='BUY' else -1
                    return stocktrade_pb2.OrderLookupResponse(order_id=order_info.order_id, status= 1, stockname=order_info.stockname,
                             trade_type=trade_type_enum, quantity=order_info.quantity)
            # if order is not present in database return status as -1
            return stocktrade_pb2.OrderLookupResponse(order_id=order_id, status = 0)
        except Exception as e:
            logger.error(f"Failed to process lookup request for request : {request} with exception: {e}")
            return stocktrade_pb2.LookupResponse(order_id=order_id, status = -1)
    
    def StreamDBUpdates(self, request, context):
        ''' 
        Funtion to send updates occured in the db to the frontend to keep the cache updated
        :param  request:  empty request
        :return response: response contains the stockname that is traded recently
        '''
        global updated_stocks_queue
        while True:
            # keep sending the updated stocknames as long as the queue is non-empty
            if (not updated_stocks_queue.empty()):
                yield stocktrade_pb2.CacheInvalidateRequest(stockname= updated_stocks_queue.get())          

    def IsAlive(self, request, context):
        ''' 
        Funtion to check if the service is alive or not from frontend
        :param  request: does not contain any field
        :return response: returns alive response with boolean True
        '''
        return stocktrade_pb2.AliveResponse(is_alive=True)

    def SetLeader(self, request, context):
        ''' 
        Funtion to set elected leader from the leader election 
        :param  request:  contains the id of the elected leader
        :return response: Empty response
        '''
        global leader_id
        leader_id = request.leader_id
        return stocktrade_pb2.Empty()


    def GetLeader(self, request, context):
        ''' 
        Funtion to get the leader from the replica order services
        :param  request:  Empty request
        :return response: respone contains the leader_id even if its 0, we will check at the request sender side for this 0 condition.
        '''
        global leader_id
        return stocktrade_pb2.GetLeaderResponse(leader_id=leader_id)


    def SyncOrderRequest(self, request, context):
        ''' 
        Funtion to sync the latest processed trade request at leader service - stores the order to the local service db
        :param  request:  contains the transaction_number, stockname, trade type and quantity
        '''
        trade_type_word = 'SELL' if request.trade_type == 1 else 'BUY'
        global service_id
        logger.info(f"Sync Order Request: {request.stockname},{trade_type_word},{request.quantity}, transaction_number: {request.transaction_number} at order-service_{service_id}")
        with lock:
            # TODO : write lock
            global curr_tran
            global stockorders_db
            curr_tran = request.transaction_number
            stockorders_db[curr_tran] = order.Order(order_id=curr_tran, stockname=request.stockname, trade_type=trade_type_word, quantity=request.quantity)
            self.write_order_to_file()
        return stocktrade_pb2.Empty()

    def SyncOrderDB(self, request, context):
        ''' 
        Funtion to sync DB data with a service that just came from crash/started
        :param  request:  contains the maximum transaction id at the restarted service
        :return response: stream of order database item containing order details
        '''
        global stockorders_db
        for k,order_info in stockorders_db.items():
            # only sends the data with transaction numbers greater than the highest transaction number of the sender service 
            if k > request.max_transaction_number:
                trade_type_enum = 1 if order_info.trade_type=='SELL' else 0 if order_info.trade_type=='BUY' else -1
                yield stocktrade_pb2.OrderDBItem(
                    stockname=order_info.stockname, trade_type=trade_type_enum, quantity=order_info.quantity, transaction_number=order_info.order_id)
    
    def replicate_order(self, transaction_number, stockname, trade_type, quantity):
        '''
        Function to send the latest successful trade order to the replica order services to maintain data sync
        '''
        # trade_type - enum format
        global service_id
        for i in range(len(config.order_ports)):
            # skips sending replicate request to self
            if i == service_id-1:
                continue
            hostAddr = config.order_hostname + ':' + str(config.order_ports[i])
            logger.info(f"Sending SyncOrderRequest to the order service replica at {hostAddr}, orderId = {transaction_number}")
            try:
                with grpc.insecure_channel(hostAddr) as channel:
                    stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
                    sync_response = stub.SyncOrderRequest(stocktrade_pb2.OrderDBItem(stockname=stockname, quantity=quantity, trade_type=trade_type, transaction_number=transaction_number))
            except Exception as e:
                logger.error(f"Failed to sync transaction with service replica at {hostAddr}, orderId= {transaction_number}\nWith exception: {e}")
        return
    
    def write_order_to_file(self):
        '''
        Function to write the last processed order to the local disk database.
        '''
        
        print("Saving order to disk", end='...')
        global stockorders_db
        global curr_tran
        global service_id
        try:
            # Adding header to the database
            if curr_tran == 1:
                dbwithheader = ['transaction_number,stockname,ordertype,quantity', stockorders_db[curr_tran].to_string()]
                with open(f'data/stockOrderDB_{service_id}.txt','w') as file:
                    file.write('\n'.join(dbwithheader))
            else:
                line = '\n' + stockorders_db[curr_tran].to_string()
                with open(f'data/stockOrderDB_{service_id}.txt','a') as file:
                    file.write(line)
            print("Done!")
        except Exception as e:
            print(f"Cannot write to the file. Failed with Exception: {e}")
