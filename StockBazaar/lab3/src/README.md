# Lab 3: Asterix and Double Trouble -- Replication, Caching, and Fault Tolerance

Install dependencies: (It is recommended to use a virtual environment.)

```
pip3 install -r /path/to/requirements.txt
```

&nbsp;

Set the project parameters through config.py file:

To run the code locally, we need to set the `mode_cloud` parameter to `False`. This is an important step because we are setting the frontend hostname based on this parameter.

The servers' hostnames and ports are already set to default values, change these if needed.

`catalog_threadpool_size` and `order_threadpool_size` are used to set the threadpool sizes in catalog and order servers respectively.

Use the `prob` parameter to set the probability with which client sends a trade request after sending a lookup request.

All the order service replica ports are given in a list `order_ports`. We assume here the IDs of the services will be same order as the port numbers (i.e., highest id service will get highest port).

We use `enable_cache` to decide whether we need to use cache or not. To use cache set it to `Y`, else set it to `N`. We can also decice on cache size by setting the value of `cache_size` parameter.

&nbsp;
&nbsp;

Once the configuration parameters are set, we run the microservices and client as follows (Follow the order shown below):

Run the catalog server by going to the path '/src/backend/catalog':

```
python3 catalog-service.py
```

Run the multiple instances of order server by going to the path '/src/backend/order' and running the following commands:

order-service.py takes id as input in the command line arguments. Use `-id <id_num>` to set the service id. The Ids are assumed to be in bounds between [1, number of instances]. So if a wrong id is given, you are prompted to run the command again.

```
python3 order-service.py -id <give_id_here>
```

Run the frontend server by going to the path '/src/frontend/':

```
python3 frontend-service.py
```

In another terminal or a different machine, go to client path '/src/client/' and run the following command:

We can check multiple functionalities from the client. We can check normal functionality, performance evalution etc by comments spectific method calls.

```
python3 client.py
```

&nbsp;
Using the HTTP connections, client sends lookup and trade requests to the frontend server. The frontend server inturn makes grpc connections with catalog server and leader order server to lookup the stocknames and place the trade orders on the stocks. The responses are sent back to frontend service and then to client. The leader order service in background sends the successfully processed order data to the replicas for data sync. Because of Replication and Fault Tolerance, even if one of the order services goes down, the others still process the requests correctly, hiding all the failures from the client. 

&nbsp;

To regenerate Proto files, go to '/src/shared/proto/' and run:

```
python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. stocktrade.proto
```
update the following import in stocktrade_pb2_grpc.py file

Replace
```
import stocktrade_pb2 as stocktrade__pb2
```
With
```
import sys
sys.path.append('../../..')
from src.shared.proto import stocktrade_pb2 as stocktrade__pb2
```


## Part 2: Deploying and running the code on AWS

To deploy the code on AWS, we need to make a change in the config file. We need to set the `mode_cloud` parameter to `True`, and set the `frontend_hostname` to appropriate value.

The detailed steps to set up the AWS EC2 machine are given in the output document in docs directory. Once the machine is setup, go to the root folder and run the bash file using the following command:
```
bash run.sh
```

Now that the servers are running you can start the client from a local machine using the command:
```
python3 client.py
```


&nbsp;
## Part 3: Testing and Performance Evaluation

Performance tests were run on the application and the graphs and observations are shared in the evaluation document and output document. docs folder also contains design document which gives information about design choices. The test folder contains three files one for each service, which contains the test cases to test that particular service.

&nbsp;
## Division of Work
### Vineeth:
* Implemented Replication and Fault Tolerance
* Implemented Catalog Service
* Implemented Order Service
* Co-implemented Client
* Wrote test cases for Order service and Replication
* Performed evaluation and updating Readme

### Om:
* Implemented Cache
* Implemented Frontend service
* Implemented Proto
* Co-implemented Client
* Wrote test cases for Cache feature, Catalog and Frontend services
* Wrote design document and updating ReadMe
* Worked on AWS deployment
