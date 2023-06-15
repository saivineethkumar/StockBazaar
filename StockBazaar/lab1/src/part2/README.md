# Lab 1: Asterix and the Stock Bazaar

Install dependencies: (It is recommended to use a virtual environment.)
```
pip3 install -r /path/to/requirements.txt
```
&nbsp;
## Part 2: Implementation with gRPC and Built in Thread Pool

Set the project parameters through config.py file:

```host``` and ```port``` - set to server hostname/ip_address and port number 

```thread_pool_size``` - set to the desired pool size. Server will have these many number of worker threads to handle the incoming requests.

We can also set initial stock prices and maximum trading volume for each stock.

&nbsp;
&nbsp;

To generate proto gRPC code, go to ```/src/part2/``` and run the following command:
```
python3 -m grpc_tools.protoc -Iproto --python_out=. --pyi_out=. --grpc_python_out=. proto/stocktrade.proto
```

&nbsp;

Once the configuration parameters are set and proto files are generated, we run the server and client as follows from the path ```/src/part2/```:

Run the server: (server is started before client)
```
python3 server.py
```
In another terminal or a different machine, run the client:
```
python3 client.py
```

&nbsp;
Using gRPC framework, client will send the lookup, trade and update requests to the server and server responds with appropriate return values