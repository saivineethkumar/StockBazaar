import http.client
import json
import random
import sys
sys.path.append('../..')
from src import config

# stocks contains stocknames that we perform lookup and order requests
stocks = []

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
    print("Connecting frontend server on port: ", config.frontend_hostname,":",config.frontend_port)
    conn = http.client.HTTPConnection(config.frontend_hostname, config.frontend_port)

    # Send GET request to /stocks?stockname=<stock_name>
    print("Lookup Case: valid stock name")
    send_get_request(conn, '/stocks?stockname=stock2')      # lookup success case
    print("\nLookup Case: invalid stock name")
    send_get_request(conn, '/stocks?stockname=stock6')      # lookup failure case because stock is not present in catalog

    # Send POST request to /orders
    print("\nTrade Case: success - valid order data")
    send_post_request(conn,'/orders','stock3',25,'SELL')   # post request success case
    print("\nTrade Case: failure - trade quantity more than available stock volume")
    send_post_request(conn,'/orders','stock5',100,'BUY')   # post request failure because the trade quantity is more than available
    print("\nTrade Case: failure - invalid stock name")
    send_post_request(conn,'/orders','stock8',10,'BUY')    # post request failure because stock is not present in catalog
    print("\nTrade Case: failure - invalid trade quantity (negative)")
    send_post_request(conn,'/orders','stock1',-5,'BUY')    # post request failure because quantity is invalid
    print("\nTrade Case: failure - invalid trade type")
    send_post_request(conn,'/orders','stock1',5,'word')    # post request failure because trade type is invalid
    
    # closing connection from client
    conn.close()



def sendLookupAndOrder(stockname, prob, conn):
    ''' 
    Funtion to send a lookup request followed by a order request with probability 'prob'
    :param stockname: name of the stock that the lookup and trade are being performed on
    :param prob: probability with which an order request is sent after a lookup request
    :param conn: HTTP connection instance
    '''

    get_response = send_get_request(conn, '/stocks?stockname=' + stockname)

    if 'data' in get_response:
        if (get_response['data']['quantity']>0) and (random.randint(1,100) <= prob*100):
            # if the returned quantity is > 0, with prob we send order request
            # we select type and quantity parameters in a random manner and send post request
            type = random.choice(['BUY', 'SELL'])
            quantity = random.choice(list(range(1,config.max_order_quantity)))
            send_post_request(conn,'/orders', stockname, quantity, type)

    print("------------------------")


def testSession(nlookup, prob):
    ''' 
    Funtion to run a sequence of lookup and optional trade requests to the server
    :param nlookup: number of lookup requests that needs to be sent in the given session - user given parameter
    :param prob: probability with which an order request is sent after a lookup request - user given parameter
    '''

    print("Testing session")
    print("Connecting frontend server on port: ", config.frontend_hostname,":",config.frontend_port)
    conn = http.client.HTTPConnection(config.frontend_hostname, config.frontend_port)
    global stocks
    for i in range(nlookup):
        sendLookupAndOrder(random.choice(stocks), prob, conn)
    
    conn.close()
    print("Session completed, closing connection")


if __name__ == '__main__':
    # initializing stocks list with a set of stocknames
    stocks = ['stock'+str(i) for i in range(1,11)]
    testNormalWorking()
    print("==================================")
    testSession(config.num_session_requests, config.prob)
