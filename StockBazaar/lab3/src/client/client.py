import http.client
import json
import random
import time
import sys
sys.path.append('../..')
from src import config
from src.shared.model.order import Order

# stocks contains stocknames that we perform lookup and order requests
stocks = []
# data structure to store the list of orders placed in a session
orders_placed = []

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
        print(f"GET request: {path}\nResponse:{response_data}")   
        return response_data
    else:
        print(f"GET request: {path}\nResponse: Path not found")
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
        print(f"POST request: {data}\nResponse:{response_data}")   
        return response_data
    else:
        print(f"POST request: {path}\nResponse: Path not found")
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
    print("Lookup Case: valid stock name present in cache")
    send_get_request(conn, '/stocks?stockname=stock2')      # lookup in cache if enabled
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

    global lookuptime
    global lookup_count
    global tradetime
    global trade_count
    start = time.perf_counter()
    get_response = send_get_request(conn, '/stocks?stockname=' + stockname)
    end = time.perf_counter()
    lookuptime += end - start
    lookup_count += 1

    if 'data' in get_response:
        if (get_response['data']['quantity']>0) and (random.randint(1,100) <= prob*100):
            # if the returned quantity is > 0, with prob we send order request
            # we select type and quantity parameters in a random manner and send post request
            type = random.choice(['BUY', 'SELL'])
            quantity = random.choice(list(range(1,config.max_order_quantity)))
            start = time.perf_counter()
            order_response = send_post_request(conn,'/orders', stockname, quantity, type)
            end = time.perf_counter()
            tradetime += end - start
            trade_count += 1

            # store the sent stockname, type, and quantity along with the returned transaction number in a list.
            if order_response is not None and "data" in order_response:
                global orders_placed
                print(order_response["data"]["transaction_number"])
                orders_placed.append(Order(order_response["data"]["transaction_number"], stockname, type, quantity))

    print("------------------------")


def testSession(nlookup, prob):
    ''' 
    Funtion to run a sequence of lookup and optional trade requests to the server
    :param nlookup: number of lookup requests that needs to be sent in the given session - user given parameter
    :param prob: probability with which an order request is sent after a lookup request - user given parameter
    '''

    global orderlookup_count
    global orderlookuptime
    global orders_placed

    orders_placed = []
    print("Testing session")
    print("Connecting frontend server on port: ", config.frontend_hostname,":",config.frontend_port)
    conn = http.client.HTTPConnection(config.frontend_hostname, config.frontend_port)
    global stocks
    for i in range(nlookup):
        sendLookupAndOrder(random.choice(stocks), prob, conn)
    
    # retrieve order information all the placed orders
    print("Checking local information with order information from server")
    for order in orders_placed:
        order_id = order.order_id
        print(f"Running sanity check for order id: {order_id}" )
        start = time.perf_counter()
        order_response = send_get_request(conn, f'/orders?order-number={order_id}')
        end = time.perf_counter()
        orderlookuptime += end - start
        orderlookup_count += 1
        if order_response is not None and "data" in order_response:
            assert order_response["data"]["number"] == order_id
            assert order_response["data"]["name"] == order.stockname
            assert order_response["data"]["type"] == order.trade_type
            assert order_response["data"]["quantity"] == order.quantity
        print(f"Check complete for order id: {order_id}")
    print("Local information consistent with server")
    orders_placed = []
    conn.close()
    print("Session completed, closing connection")


def PerformanceEvaluation():
    '''
    Function to perform the performance evaluation - finds average latencies for differnt types of requests
    '''
    print("For Performance Evaluation")
    global lookuptime
    global tradetime
    global orderlookuptime
    global lookup_count
    global trade_count
    global orderlookup_count
    lookuptime = 0
    tradetime = 0
    orderlookuptime = 0
    lookup_count = 0
    trade_count = 0
    orderlookup_count = 0
    
    num_session_requests = 500
    eval_output = "For Performance Evaluation\n"
    for prob in [0,0.2,0.4,0.6,0.8,1]:
        print("============================================")
        print(f"For prob: {prob}")
        eval_output += "============================================\n" + f"For prob: {prob}\n"
        testSession(num_session_requests, prob)

        lookup_latency_per_req = lookuptime/lookup_count
        trade_latency_per_req = tradetime/trade_count if trade_count !=0 else 0
        orderlookup_latency_per_req = orderlookuptime/orderlookup_count if orderlookup_count !=0 else 0

        print('lookup: {:.6f}s per request'.format(lookup_latency_per_req))
        print('trade: {:.6f}s per request'.format(trade_latency_per_req))
        print('orderlookup: {:.6f}s per request'.format(orderlookup_latency_per_req))
        print("============================================")

        eval_output += 'lookup: {:.6f}s per request\n'.format(lookup_latency_per_req)
        eval_output += 'trade: {:.6f}s per request\n'.format(trade_latency_per_req)
        eval_output += 'orderlookup: {:.6f}s per request\n'.format(orderlookup_latency_per_req)
        eval_output += ("============================================\n")
        print(eval_output)

def CachePerformance():
    print("Cache Performance evaluation")
    global stocks

    request_types = ['Lookup', 'Trade','OrderLookup']
    num_session_requests = 2000
    totaltime = 0
    count = 0

    conn = http.client.HTTPConnection(config.frontend_hostname, config.frontend_port)
    for _ in range(num_session_requests):
        request_type = random.choice(request_types)
        if request_type == 'Lookup':
            stockname = random.choice(stocks)
            start = time.perf_counter()
            send_get_request(conn, '/stocks?stockname=' + stockname)
            end = time.perf_counter()
            totaltime += end - start
            count +=1
        elif request_type == 'Trade':
            stockname = random.choice(stocks)
            trade_type = random.choice(['BUY', 'SELL'])
            quantity = random.choice(list(range(1,config.max_order_quantity)))
            send_post_request(conn,'/orders', stockname, quantity, trade_type)
        else:
            order_id = random.randint(1,200)
            send_get_request(conn, f'/orders?order-number={order_id}')

    print(f"cache status: {config.enable_cache}")
    latency_per_req = totaltime/count if count !=0 else 0
    print('lookup latency: {:.6f} s per request'.format(latency_per_req))


if __name__ == '__main__':
    # initializing stocks list with a set of stocknames
    stocks = ['stock'+str(i) for i in range(1,12)]
    testNormalWorking()
    # print("==================================")
    # testSession(config.num_session_requests, config.prob)
    # PerformanceEvaluation()