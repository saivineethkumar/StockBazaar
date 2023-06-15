from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import socketserver
import grpc
import sys
sys.path.append('../..')

from src.shared.util import logging
from src import config
from src.shared.proto import stocktrade_pb2
from src.shared.proto import stocktrade_pb2_grpc



class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


class Handler(BaseHTTPRequestHandler):
    #setting HTTP protocol version to 1.1
    protocol_version = 'HTTP/1.1'
    def do_GET(self):
        '''
        overriding function do_GET to handle get requests
        '''
        #get path and request parameters from url
        path, request_params = self._parse_url()
        if (path == '/hello'):
            # /hello?name=<> path. Return a hello response
            name = request_params.get('name', [None])[0]
            message = f"Hello, {name}!"
            self._send_response(message)
        elif (path == '/stocks'):
            #handle /stock?stockname=<> endpoint. Requests to this url are used to perform lookup on a stockname
            stockname = request_params.get('stockname', [None])[0] #get stockname from query parameters
            response = lookup(stockname) #perform lookup on the stockname
            self._send_response(response) #send http response
        else:
            #Send 404 error for all other paths
            logger.warning(f'Path does not exist : {path}')
            self.send_error(404)

    def do_POST(self):
        #get path from url
        path, _ = self._parse_url()
        #get request body
        request_body = self._get_request_body()
        if (path == '/orders'):
            #handle /orders endpoint. Used to perform a trade on a stock
            response = trade(request_body['name'],request_body['quantity'], request_body['type']) #perform trade on the stockname
            self._send_response(response) #send http response
        else:
             #Send 404 error for all other paths
            logger.warning(f'Path does not exist : {path}')
            self.send_error(404)

    def log_message(self, format, *args):
        #Overriding function to use custom logging
        logger.info('%s %s', self.address_string(), format % args)

    def _parse_url(self):
        '''
        Function to parse url
        return path: the base path in the url
        return request_params: the request parameters in the path
        '''
        parsed_url = urlparse(self.path)
        base_path = parsed_url.path
        request_params = parse_qs(parsed_url.query)
        return base_path, request_params

    def _get_request_body(self):
        '''
        Function to read request body and parse json
        return request body: the json request body
        '''
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(body)
        except Exception as e:
            logger.error(f'Failed to read request body with exception: {e}')

    def _send_response(self, response):
        '''
        Function to send http response to client
        '''
        response = response.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)


def lookup(stockname):
    '''
    Function to initiate lookup on a stock
    :param stockname: name of the stock to initiate lookup on
    '''
    logger.info(f"Sending lookup request for : {stockname}")
    try:
        #call catalog service
        hostAddr = config.catalog_hostname + ':' + str(config.catalog_port)
        with grpc.insecure_channel(hostAddr) as channel:
            stub = stocktrade_pb2_grpc.CatalogServiceStub(channel)
            lookup_response = stub.Lookup(stocktrade_pb2.LookupRequest(stockname= stockname))
            logger.info(
                f"Lookup request: {lookup_response.stockname}, response: Price of stock: {lookup_response.price}, Volume of the stock: {lookup_response.volume}")
            if lookup_response.price != -1:
                response =  {
                    'name' : lookup_response.stockname,
                    'price' : lookup_response.price,
                    'quantity' : lookup_response.volume
                }
                return get_http_response(response) #prepare http response
            else:
                return get_http_error_response(404, 'stock not found') #prepare http error response
    except Exception as e:
        logger.error(f"Failed to get lookup response for {stockname} with expception: {e}") 
    return get_http_error_response(404, 'Internal Server Error')

def trade(stockname, quantity, trade_type):
    '''
    Function to initiate trade on a stock
    :param stockname: name of the stock to initiate trade on
    :param quantity: quantity being traded
    :param trade_type: type of the trade. BUY or SELL
    '''
    logger.info(f"Sending trade request of type: {trade_type} for : {stockname} with quantity: {quantity}")
    try:
        #call order service
        hostAddr = config.order_hostname + ':' + str(config.order_port)  
        with grpc.insecure_channel(hostAddr) as channel:
            stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
            order_response = stub.Trade(stocktrade_pb2.TradeRequest(
                stockname=stockname, quantity=quantity, trade_type=trade_type))
            logger.info(
                f"Trade request: {stockname}, {quantity}, response status : {order_response.status}")
            if (order_response.status == 1):
                response = {
                    'transaction_number' : order_response.transaction_number
                }
                return get_http_response(response) #prepare http response
            elif (order_response.status == 0):
                return get_http_error_response(404, 'Trading not permitted due to insufficient volume') #prepare order response
            else:
                return get_http_error_response(404, 'Stock not found')
    except Exception as e:
        logger.error(f"Failed to get trade response for {stockname} with exception: {e}")
        return get_http_error_response(404, 'Internal Server Error')

#TODO: remove the function (not using)
def save_file():
    '''
    Function to call save files before exiting.
    '''
    hostAddr = config.order_hostname + ':' + str(config.order_port)  
    with grpc.insecure_channel(hostAddr) as channel:
        stub = stocktrade_pb2_grpc.OrderServiceStub(channel)
        stub.Save(stocktrade_pb2.Empty())
        

def get_http_response(response):
    '''
    Function to prepare http response.
    Response is of the structure {'data' : response}
    '''
    response = {
            'data': response
        }
    return convert_to_json(response)

def get_http_error_response(error_code, error_message):
    '''
    Function to error http response.
    Response is of the structure {'error' : {'code' : ..., 'message' : ...}}
    '''
    response = {
        'error': {
            'code': error_code,
            'message': error_message
        }
    }
    return convert_to_json(response)

def convert_to_json(obj):
    '''
    Function to convert python object to json.
    return json object: the json equivalent of the python object
    '''
    try:
        json_obj = json.dumps(obj)
        return json_obj
    except Exception as e:
        return None


if __name__ == "__main__":
    #create a custom logger for frontend service
    logger = logging.logger('frontend-service')
    hostname = '0.0.0.0' 
    port = config.frontend_port
    webServer = ThreadedHTTPServer((hostname, port), Handler)
    logger.info("Server started http://%s:%s" % (hostname, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    # atexit.register(save_file)
    webServer.server_close()
    logger.warning("Server stopped.")
