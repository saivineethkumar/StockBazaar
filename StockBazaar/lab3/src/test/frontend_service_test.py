import http.client
import time
import json
import unittest

FRONTEND_HOSTNAME = 'localhost'     # hostname on which frontend server is hosted
FRONTEND_PORT = 26111               # port on which frontend server is serving
N_REQ = 500                         # Number of request to send while checking the response latencies (2*N_REQ number of requests will be sent)
INVALID_ORDER_ID = -1

def send_get_request(conn, path):
    ''' 
    Funtion to send GET request to the frontend server
    :param conn: HTTP connection instance
    :param path: url which looks up a given stockname
    :return response_data: returns the lookup response from the server in the form of json object 
    '''
    conn.request('GET',path)            # send GET request
    response = conn.getresponse()       # receive response and convert it to json object
    if response.status == 200:
        response_data = json.loads(response.read().decode())
        print(
            f"GET request: {path}\nResponse:{response_data}")   
        return response_data
    else:
        print(
            f"GET request: {path}\nResponse: Path not found")
        return None


def send_post_request(conn, path, stockname, quantity, type):
    ''' 
    Funtion to send POST request to the frontend server
    :param conn: HTTP connection instance
    :param path: url which performs trade with the given data
    :param stockname: name of the stock that the trade is being performed on
    :param quantity: amount of stock order that is being traded
    :param type: SELL or BUY order type
    :return response_data: returns the order response from the server in the form of json object 
    '''

    # order request parameters
    data = {
        'name':stockname,
        'quantity':quantity,
        'type':type
    }

    json_data = json.dumps(data).encode()
    headers = {'Content-type': 'application/json','Content-Length':len(json_data)}   # headers for the request
    conn.request('POST', path, body=json_data, headers=headers)                      # send GET request   
    response = conn.getresponse()                                                    # receive response and convert it to json object
    if response.status == 200:
        response_data = json.loads(response.read().decode())
        print(
            f"POST request: {data}\nResponse:{response_data}")   
        return response_data
    else:
        print(
            f"POST request: {path}\nResponse: Path not found")
        return None



def testNormalWorking():
    ''' 
    Funtion to test the normal behavior of our system
    '''

    print("Testing normal working")
    print("Connecting frontend server on port: ", FRONTEND_HOSTNAME,":",FRONTEND_PORT)
    conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)

    # Send GET request to /stocks?stockname=<stock_name>
    print("Lookup Case: valid stock name")
    send_get_request(conn, '/stocks?stockname=stock2')      # lookup success case
    print("\nLookup Case: invalid stock name")
    send_get_request(conn, '/stocks?stockname=stock6')      # lookup failure case because stock is not present in catalog

    # Send POST request to /orders
    print("\nTrade Case: success - valid order data")
    send_post_request(conn,'/orders','stock3',25,'SELL')   # post request success case
    print("\nTrade Case: failure - trade quantity more than available stock volume")
    send_post_request(conn,'/orders','stock5',100,'BUY')   # post request failure because the trade quantity is more than available volume
    print("\nTrade Case: failure - invalid stock name")
    send_post_request(conn,'/orders','stock8',10,'BUY')    # post request failure because stock is not present in catalog
    print("\nTrade Case: failure - invalid trade quantity (negative)")
    send_post_request(conn,'/orders','stock1',-5,'BUY')    # post request failure because quantity is invalid
    print("\nTrade Case: failure - invalid trade type")
    send_post_request(conn,'/orders','stock1',5,'word')    # post request failure because trade type is invalid


    # closing connection from client
    conn.close()


def testLookupLatency():
    '''
    Function to send Lookup requests sequentially to server
    '''
    print("Testing Lookup Latency")
    conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
    start = time.perf_counter()
    # Number of requests to test the latency can be changed by changing N_REQ
    for i in range(N_REQ):
        send_get_request(conn,'/stocks?stockname=stock2')
        send_get_request(conn,'/stocks?stockname=stock6')
    end = time.perf_counter()
    totalTime = end - start
    latency_per_req = totalTime/(2*N_REQ)
    print('{:.6f}s per request'.format(latency_per_req))

    # closing connection from client
    conn.close()
    


def testTradeLatency():
    '''
    Function to send Trade requests sequentially to server
    '''
    print("Testing Trade Latency")
    conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
    start = time.perf_counter()
    # Number of requests to test the latency can be changed by changing N_REQ
    for i in range(N_REQ):
        send_post_request(conn,'/orders','stock1',1,'BUY')
        send_post_request(conn,'/orders','stock4',2,'SELL')
    end = time.perf_counter()
    totalTime = end - start
    latency_per_req = totalTime/(2*N_REQ)
    print('{:.6f}s per request'.format(latency_per_req))

    # closing connection from client
    conn.close()

class TestFrontendService(unittest.TestCase):
    def test_lookup_success_response(self):
        '''
        Function to test lookup success response
        '''
        print("Test Lookup Success")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        lookup_response = send_get_request(conn,'/stocks?stockname=stock1')
        self.assertTrue(lookup_response != None)
        self.assertTrue('data' in lookup_response)
        self.assertTrue(lookup_response['data']['name'] == 'stock1')
        conn.close()
        

    def test_lookup_stockname_failure_response(self):
        '''
        Function to test lookup failure response
        '''
        print("Test Lookup Failure because of invalid stockname")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        lookup_response = send_get_request(conn,'/stocks?stockname=stock10')
        self.assertTrue(lookup_response != None)
        self.assertTrue('error' in lookup_response)
        self.assertTrue(lookup_response['error']['code'] == 404)
        conn.close()
    

    def test_lookup_path_failure_response(self):
        '''
        Function to test lookup failure response
        '''
        print("Test Lookup Failure because of invalid path")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        lookup_response = send_get_request(conn,'/stock?stockname=stock1')
        self.assertTrue(lookup_response == None)
        conn.close()

    
    def test_order_success_response(self):
        '''
        Function to test order success response
        '''
        print("Test Order Success")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock3',25,'SELL')
        self.assertTrue(order_response != None)
        self.assertTrue('data' in order_response)
        self.assertTrue('transaction_number' in order_response['data'])
        self.assertTrue( order_response['data']['transaction_number'] > 0)
        conn.close()

    def test_order_transaction_failure_response(self):
        '''
        Function to test order failure response
        '''
        print("Test Order Failure because trade quantity more than available volume")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock5',100,'BUY')
        self.assertTrue(order_response != None)
        self.assertTrue('error' in order_response)
        self.assertTrue(order_response['error']['code'] == 404)
        conn.close()

    def test_order_stockname_failure_response(self):
        '''
        Function to test order failure response
        '''
        print("Test Order Failure because of invalid stockname")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock8',10,'BUY')
        self.assertTrue(order_response != None)
        self.assertTrue('error' in order_response)
        self.assertTrue(order_response['error']['code'] == 404)
        conn.close()

    def test_order_invalid_quantity_failure_response(self):
        '''
        Function to test order failure response
        '''
        print("Test Order Failure because of invalid trade quantity")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock1',-5,'BUY')
        self.assertTrue(order_response != None)
        self.assertTrue('error' in order_response)
        self.assertTrue(order_response['error']['code'] == 404)
        conn.close()

    def test_order_tradetype_failure_response(self):
        '''
        Function to test order failure response
        '''
        print("Test Order Failure because of invalid trade type")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock1',5,'word')
        self.assertTrue(order_response != None)
        self.assertTrue('error' in order_response)
        self.assertTrue(order_response['error']['code'] == 404)
        conn.close()

    def test_lookup_from_cache(self):
        '''
        Function to test cache
        '''
        print("Test second lookup request should return from cache")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        #Initial request sent to catalog service
        lookup_response = send_get_request(conn,'/stocks?stockname=stock2')
        self.assertTrue(lookup_response != None)
        self.assertTrue('data' in lookup_response)
        self.assertTrue(lookup_response['data']['name'] == 'stock2')

        #Second request sent to cache
        lookup_response_cache = send_get_request(conn,'/stocks?stockname=stock2')
        self.assertTrue(lookup_response_cache != None)
        self.assertTrue('data' in lookup_response_cache)
        self.assertTrue(lookup_response['data']['name'] == lookup_response['data']['name'])
        self.assertTrue(lookup_response['data']['price'] == lookup_response['data']['price'])
        self.assertTrue(lookup_response['data']['quantity'] == lookup_response['data']['quantity'])
        conn.close()

    def test_order_lookup_success_response(self):
        '''
        Function to test order lookup of an existing order
        '''
        print("Test order get request for an already existing order")
        #precondition checks to ensure order is present in db
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_response = send_post_request(conn,'/orders','stock1',25,'SELL')
        self.assertTrue(order_response != None)
        self.assertTrue('data' in order_response)
        self.assertTrue('transaction_number' in order_response['data'])
        order_id = order_response['data']['transaction_number']

        # perfrom lookup on the above order id
        order_lookup_response = send_get_request(conn, f'/orders?order-number={order_id}')
        self.assertTrue(order_lookup_response is not None)
        self.assertTrue('data' in order_lookup_response)
        self.assertTrue('name' in order_lookup_response['data'])
        self.assertTrue('number' in order_lookup_response['data'])
        self.assertTrue('type' in order_lookup_response['data'])
        self.assertTrue('quantity' in order_lookup_response['data'])

        self.assertTrue(order_lookup_response['data']["name"] == 'stock1')
        self.assertTrue(order_lookup_response['data']['number'] == order_id)
        self.assertTrue(order_lookup_response['data']['type'] == 'SELL')
        self.assertTrue(order_lookup_response['data']['quantity'] == 25)
        conn.close()

    def test_order_lookup_failure_response(self):
        '''
        Function to test failure scenario of order lookup
        '''
        print("Test order get request for an invalid order")
        conn = http.client.HTTPConnection(FRONTEND_HOSTNAME, FRONTEND_PORT)
        order_lookup_response = send_get_request(conn, f'/orders?order-number={INVALID_ORDER_ID}')
        self.assertTrue(order_lookup_response != None)
        self.assertTrue('error' in order_lookup_response)
        self.assertTrue(order_lookup_response['error']['code'] == 404)
        conn.close()
    
   
if __name__ == '__main__':
    testNormalWorking()
    # testLookupLatency()
    # testTradeLatency()

    # Unit test cases to test the frontend service working
    unittest.main()
    