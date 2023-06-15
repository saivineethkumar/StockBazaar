import time
import threading

def lookUpLatency(N, socketComm, stockname):
    """
    Making requests sequentially

    """
    start = time.perf_counter()
    for i in range(N):
        socketComm(stockname)
    end = time.perf_counter()
    latency = end - start
    avgLatency = latency/N
    print(f"Latency for {N} lookup requests: {latency}, average request latency: {avgLatency}")
    return (latency, avgLatency)
