# Lab 1: Asterix and the Stock Bazaar

Install dependencies: (It is recommended to use a virtual environment.)

```
pip3 install -r /path/to/requirements.txt
```

&nbsp;

## Part 1: Implementation with Socket Connection and Handwritten Thread Pool

Set the project parameters through config.py file:

`host` and `port` - set to server hostname/ip_address and port number

`thread_pool_size` - set to the desired pool size. Server will have these many number of worker threads to handle the incoming requests.

We can also set initial stock prices and maximum trading volume for each stock.

&nbsp;
&nbsp;

Once the configuration parameters are set, we run the server and client as follows from the path `/src/part1/`:

Run the server: (server is started before client)

```
python3 server.py
```

In another terminal or a different machine, run the client:

```
python3 client.py
```

&nbsp;
Using socket communication, client will send the lookup requests to the server and server responds with the price if stock is valid or -1 if stock is invalid or 0 if stock is valid but suspended.

&nbsp;

## Part 2: Implementation with gRPC and Built in Thread Pool

Set the project parameters through config.py file:

`host` and `port` - set to server hostname/ip_address and port number

`thread_pool_size` - set to the desired pool size. Server will have these many number of worker threads to handle the incoming requests.

We can also set initial stock prices and maximum trading volume for each stock.

&nbsp;
&nbsp;

To generate proto gRPC code, go to `/src/part2/` and run the following command:

```
python3 -m grpc_tools.protoc -Iproto --python_out=. --pyi_out=. --grpc_python_out=. proto/stocktrade.proto
```

&nbsp;

Once the configuration parameters are set and proto files are generated, we run the server and client as follows from the path `/src/part2/`:

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

## Division of Work
### Vineeth:
* Implemented Thread pool in Part1
* Implemented Client and Server for Part1
* Co-implemented the Proto for Part2
* Helped with client-server code in Part2
* Performed evaluation on Part1

### Om:
* Implemented Client and Server in Part2
* Implemented Stock model
* Co-implemented the Proto for Part2
* Helped with Thread pool implementation in Part1
* Performed evaluation on Part2
