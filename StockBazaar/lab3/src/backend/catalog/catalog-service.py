from concurrent import futures
import grpc
from threading import Lock
import atexit
import sys
sys.path.append('../../..')
from src.shared.model import stock
from src import config
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc
from src.shared.util import logging

stocks_db = {}      # stocks db to store the stock objects present in the catalog
lock = Lock()       # lock to access the above global variables


class CatalogService(stocktrade_pb2_grpc.CatalogServiceServicer):

    def Lookup(self, request, context):
        ''' 
        Funtion to return the price and the trading volume of a stock
        :param  request:  contains the name of the stock to perform lookup on
        :return response: contains the name, price and volume of the stock if present in catalog, other price and volume are set to -1 and returned
        '''
        try:

            name = request.stockname  # name of the stock to perform lookup on
            logger.info(f'Received lookup request for : {name} on catalog service')
            # if stock is present in database return price and volume from db
            global stocks_db
            if name in stocks_db:
                with lock:
                    # TODO: read lock
                    stock = stocks_db[name]
                    return stocktrade_pb2.LookupResponse(stockname=name,price=stock.getPrice(), volume=stock.volume)
            # if stock is not present in database return price and volume as -1
            return stocktrade_pb2.LookupResponse(stockname=name,price=-1, volume=-1)
        except Exception as e:
            logger.error(f"Failed to process lookup request for request : {request} with exception: {e}")
            return stocktrade_pb2.LookupResponse(stockname=name,price=-1, volume=-1)


    def Update(self, request, context):
        '''
        Function to perform trading on a stock
        :param request: contains the name,quantity and trade_type of the given order
        :return response: contains the name, tradestatus: 1 if trading is succesfull, 0 if trading is suspended, -1 otherwise
        '''
        try:
            name = request.stockname  # name of the stock that is being traded
            quantity = request.quantity  # quantity being traded
            trade_type = request.trade_type  # type of trade (BUY or SELL)
            logger.info(f'Received Update request with quantity: {quantity} of type: {trade_type} for : {name} on catalog service')
            global stocks_db
            if name in stocks_db:
                with lock:
                    # TODO: write lock
                    stock = stocks_db[name]
                    # call the trade function on stock to perform trading
                    trade_status = stock.trade(quantity=quantity, trade_type=trade_type)
                    dump_to_disk()
                    # print("trade status:", trade_status)

                # return trade_status 1 if trade is successfull and 0 otherwise
                return stocktrade_pb2.UpdateResponse(stockname=name,status=trade_status)
        except Exception as e:
            logger.error(f"Failed to process update request in catalog for request : {request} with exception: {e}")
        # return trade_status -1 if stock is invalid or the function fails
        return stocktrade_pb2.UpdateResponse(stockname=name,status=-1)



def serve(hostAddr):
    ''' 
    Funtion that starts catalog server on the given port and serves incoming requests
    :param hostaddr: the host and port on which the catalog service is serving requests
    '''
    logger.info(f"Catalog-service serving on port: {hostAddr}")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=config.catalog_threadpool_size))
    stocktrade_pb2_grpc.add_CatalogServiceServicer_to_server(CatalogService(), server)
    # to connect between 2 machines, keep the server hostname here eg: "elnux3.cs.umass.edu:50051"
    server.add_insecure_port(hostAddr)
    server.start()
    server.wait_for_termination()


def load_stocks_db():
    '''
    Function to initilize in-memory database from local disk database
    '''
    
    logger.info("Loading stocks info from local disk database...")
    # add the stock objects to db
    global stocks_db
    stocks_db = {}
    try:
        with open('data/stockDB.txt') as file:
            # to skip the first line
            file.readline()
            for line in file:
                stockname,price,currvol =line.rstrip().split(',')
                stockname, price, currvol = stockname.strip(), float(price.strip()), int(currvol.strip())
                stocks_db[stockname] = stock.Stock(stockname, price, currvol)
        logger.info("Done!")
    except Exception as e:
        logger.error(f"Cannot read the text, please make sure the formatting in the file is correct\nException: {e}")


def dump_to_disk():
    '''
    Function to write back to the local disk database.
    '''
    
    logger.info("Saving data to disk...")
    
    global stocks_db
    header = ['stockname,price,currvol']  # header to write to the text file

    lines = header + [value.to_string() for _, value in stocks_db.items()]
    try:
        with open('data/stockDB.txt','w') as file:
            file.write('\n'.join(lines))
        logger.info("Done!")
    except Exception as e:
        logger.error(f"Cannot write to the file.Failed with Exception: {e}")

    

if __name__ == '__main__':
    logger = logging.logger('catalog-service')
    try:
        # initialize database
        load_stocks_db()
        # start the server on hostAddr to receive requests
        hostAddr = config.catalog_hostname + ':' + str(config.catalog_port)
        serve(hostAddr)
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt")
    except Exception as e:
        logger.error(f"Exiting with exception: {e}")

    # calls the funtion to write back to disk when exiting the server
    atexit.register(dump_to_disk)
