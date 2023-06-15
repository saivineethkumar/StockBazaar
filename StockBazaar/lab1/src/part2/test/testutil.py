import client
import time
import threading
import stocktrade_pb2

stocks_list = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo']


def testLookupFunctionsSeq(N):
    '''
    Function to send Lookup requests sequentially to server
    '''
    start = time.perf_counter()
    for i in range(N):
        client.lookup('GameStart')
    end = time.perf_counter()
    totalTime = end - start
    latency_per_req = totalTime/N
    print('{:.6f}s per request'.format(latency_per_req))


def testTradeFunctionsSeq(N):
    '''
    Function to send Trade requests sequentially to server
    '''
    start = time.perf_counter()
    for i in range(N):
        client.trade('GameStart', 1, 'BUY')
    end = time.perf_counter()
    totalTime = end - start
    latency_per_req = totalTime/N
    print('{:.6f}s per request'.format(latency_per_req))


def testupdateFunctionsSeq(N):
    '''
    Function to send Update requests sequentially to server
    '''
    start = time.perf_counter()
    for i in range(N):
        client.update('GameStart', 101.45)
    end = time.perf_counter()
    totalTime = end - start
    latency_per_req = totalTime/N
    print('{:.6f}s per request'.format(latency_per_req))


def testAllFunctionsSeq():
    '''
    Function to send all requests sequentially to server
    '''
    client.update('GameStart', 100)
    client.trade('GameStart', 1, 'BUY')
    client.lookup('GameStart')


def testAllFunctionsConcurrently(N):
    '''
    Function to send requests concurrently to server
    '''
    threads = []
    # creating threads and sending requests concurrently
    for i in range(N):
        thread1 = threading.Thread(
            target=client.update, args=('FishCo', 10.9999))
        thread1.start()
        threads.append(thread1)
        thread2 = threading.Thread(target=client.trade, args=(
            'FishCo', 30, stocktrade_pb2.BUY))
        thread2.start()
        threads.append(thread2)
        thread3 = threading.Thread(target=client.lookup, args=('FishCo',))
        thread3.start()
        threads.append(thread3)

    for thread in threads:
        thread.join()
