from concurrent import futures

import grpc
import argparse
from threading import Lock
import atexit
import sys
sys.path.append('../../..')
from src import config
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc
from src.shared.util import logging
from src.shared.model import order
import order_service_pb2

lock = Lock()           # lock to access the above global variables

def serve(hostAddr):
    ''' 
    Funtion that starts order server on the given port and serves incoming requests
    :param hostaddr: the host and port on which the order service is serving requests
    '''
    logger.info(f"Order-service serving on port: {hostAddr}")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=config.order_threadpool_size))
    stocktrade_pb2_grpc.add_OrderServiceServicer_to_server(order_service_pb2.OrderService(), server)
    # to connect between 2 machines, keep the server hostname here with port eg: "elnux3.cs.umass.edu:50051"
    server.add_insecure_port(hostAddr)
    server.start()
    # Call to Sync the database on restart (from crash)
    syncDBOnStart()
    logger.info(f"Starting server...")
    server.wait_for_termination()


def load_stockorders_db():
    '''
    Function to initilize in-memory database from local disk database
    '''
    
    logger.info("Loading stock orders from local disk database")
    # add the stock objects to db
    # global service_id
    order_service_pb2.stockorders_db = {}
    order_service_pb2.curr_tran = 0
    try:
        # Data is stored in the respective service file of service id. Each replica has a db of its own
        with open(f'data/stockOrderDB_{order_service_pb2.service_id}.txt') as file:
            # to skip the first line - first line is header
            file.readline()
            for line in file:
                trans_num,stockname,type,quantity =line.rstrip().split(',')
                trans_num,stockname,type,quantity = int(trans_num.strip()), stockname.strip(), type.strip(), int(quantity.strip())
                order_service_pb2.stockorders_db[trans_num] = order.Order(order_id=trans_num, stockname=stockname, trade_type=type, quantity=quantity)
                order_service_pb2.curr_tran = max(order_service_pb2.curr_tran,trans_num)
        logger.info("Done!")
    except FileNotFoundError as e:
        # service started for the first time, file not present. File will be created when we start storing transactions
        logger.error(f"DB file is not present, starting server for the first time. File will be created if a trade happens\nException: {e}")
    except Exception as e:
        logger.error(f"cannot read the text, please make sure the formatting in the file is correct\nException: {e}")
    

def dump_to_disk():
    '''
    Function to write back to the local disk database.
    '''
    
    logger.info("Saving data to disk...")
    # global service_id
    try:
        # Adding header to the database
        header = ['transaction_number,stockname,ordertype,quantity'] 
        lines = header + [value.to_string() for value in order_service_pb2.stockorders_db.values()]
        # Data is stored in the respective service file of service id. Each replica has a db of its own
        # File will be created if its not present
        with open(f'data/stockOrderDB_{order_service_pb2.service_id}.txt','w') as file:
            file.write('\n'.join(lines))
        logger.info("Done!")
    except Exception as e:
        logger.error(f"Cannot write to the file.Failed with Exception: {e}")


def syncDBOnStart():
    '''
    Syncs the DB from the leader service on start (restarted from crash)
    Function first gets the leader from one of the available order services, then gets the data from that leader service. 
    If leader is not elected yet, meaning we are starting servers for the first time so no sync happens.
    '''
    
    logger.info("Syncing database...")
    # global service_id
    
    # Finding leader 
    order_service_pb2.leader_id = 0      # resetting leader_id to avoid discrepancies
    for i in range(len(config.order_ports)-1, -1,-1):
        if i == order_service_pb2.service_id-1:
            continue
        try:
            hostAddr = config.order_hostname + ':' + str(config.order_ports[i])
            logger.info(f"Sending GetLeader to the order service instance at {hostAddr}")
            with grpc.insecure_channel(hostAddr) as channel:
                stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
                getleader_response = stub.GetLeader(stocktrade_pb2.Empty())
                # If the response contains a non zero leader id value then we can say the leader is found
                if getleader_response.leader_id != 0:
                    order_service_pb2.leader_id = getleader_response.leader_id
                    break
        except grpc.RpcError as rpc_error:
            # If a particular replica service is not available, we will skip it and send getleader request to next replica
            if rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logger.error(f"Order service instance at {hostAddr} is not alive/unavailable")
            else:
                logger.error(f" Failed to connect the Order service instance at {hostAddr}\nException: {rpc_error}")
        except Exception as e:
            logger.error(f" Failed to connect the Order service instance at {hostAddr}\nException: {e}")

    # leader not found or did not elect yet - so not syncing
    if order_service_pb2.leader_id == 0:
        return
    
    # Syncing DB with the leader service
    try:
        hostAddr = config.order_hostname + ':' + str(config.order_ports[order_service_pb2.leader_id-1])
        logger.info(f"Syncing data from the Leader order service instance at {hostAddr}")
        with grpc.insecure_channel(hostAddr) as channel:
            stub = stocktrade_pb2_grpc.OrderServiceStub(channel)            
            with lock:
                # looping through the stream response from the leader service
                for orderDBItem in stub.SyncOrderDB(stocktrade_pb2.SyncRequest(max_transaction_number=order_service_pb2.curr_tran)):
                    trade_type_word = 'SELL' if orderDBItem.trade_type == 1 else 'BUY'
                    # current transaction has to be updated too so that new transactions will be continued from the latest transaction number
                    order_service_pb2.curr_tran = max(order_service_pb2.curr_tran, orderDBItem.transaction_number)
                    order_service_pb2.stockorders_db[orderDBItem.transaction_number] = order.Order(
                        order_id=orderDBItem.transaction_number, stockname=orderDBItem.stockname, trade_type=trade_type_word, quantity=orderDBItem.quantity)
            # TODO: should we keep dump to disk in the lock or not
            dump_to_disk()
            return
    except Exception as e:
        logger.error(f" Failed to connect the Order service instance at {hostAddr}\nException: {e}")
        logger.error(f"Resyncing the database")
        # If the leader service is not present or some exception happens, we will retry the syncing process hoping an alive leader is elected and broadcasted.
        syncDBOnStart()
    return


def getHostAddr():
    # returns the host address for the order service based on its service_id from the config
    # global service_id
    if order_service_pb2.service_id >= config.minID and order_service_pb2.service_id <= config.maxID:
        return config.order_hostname + ':' + str(config.order_ports[order_service_pb2.service_id-1])
    else:
        print("Invalid order service id number")
        return ""

if __name__ == '__main__':
    try:
        logger = logging.logger('order-service')
        # command line arguments for reading ID number of a order server instance
        parser = argparse.ArgumentParser(description='OrderService')
        parser.add_argument('-id', type=int, default=-1, help='input order service id for this instance')
        args = parser.parse_args()
        
        # We want the given service id to be in bounds to the min, max given in the config file - having bounds will make automating the system easy
        if args.id >= config.minID  and args.id <= config.maxID:
            # global service_id
            order_service_pb2.service_id = args.id
            # initialize database
            load_stockorders_db()
            # start the server on hostAddr to receive requests
            hostAddr = getHostAddr()
            serve(hostAddr)
        else:
            # -id missing or out of bounds
            print(f"Order service id is either missing or not in bounds, please start service with a valid ID between {config.minID} and {config.maxID}")
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt")
    except Exception as e:
        logger.error(f"Exiting with exception: {e}")