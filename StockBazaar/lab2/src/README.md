# Lab 2: Asterix and the Microservice Stock Bazaar

Install dependencies: (It is recommended to use a virtual environment.)

```
pip3 install -r /path/to/requirements.txt
```

&nbsp;

## Part 1: Implement Your Two-Tiered Stock Bazaar as Microservices

Set the project parameters through config.py file:

Set `mode_docker` to `True` while running the microservices with Docker. When running the services on the local machine, set this to `False`.

The servers' hostnames and ports are already set to default values, change these if needed.

`catalog_threadpool_size` and `order_threadpool_size` are used to set the threadpool sizes in catalog and order servers respectively.

Use the `prob` parameter to set the probability with which client sends a trade request after sending a lookup request.

&nbsp;
&nbsp;

Once the configuration parameters are set, we run the microservices and client as follows (servers are started before client):

Run the frontend server by going to the path '/src/frontend/':

```
python3 frontend-service.py
```

Run the catalog server by going to the path '/src/backend/catalog':

```
python3 catalog-service.py
```

Run the order server by going to the path '/src/backend/order':

```
python3 order-service.py
```

In another terminal or a different machine, go to client path '/src/client/' and run:

```
python3 client.py
```

&nbsp;
Using the HTTP connections, client sends lookup and trade requests to the frontend server. The frontend server inturn makes grpc connections with catalog and order servers to lookup the stocknames and place the trade orders on the stocks. The responses are sent back to frontend service and then to client.

&nbsp;

To regenerate Proto files, go to '/src/shared/proto/' and run:

```
python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. stocktrade.proto
```
update the following import in stocktrade_pb2_grpc.py file

```
import sys
sys.path.append('../../..')
from src.shared.proto import stocktrade_pb2 as stocktrade__pb2
```

## Part 2: Containerize Your Application

To containerize the application, we have created three Dockers for the three microservices. We can run the application either by building and running the dockers manually or use docker-compose to build and run them using docker-compose up and down.

To use the application with docker, first set the config parameter `mode_docker` to `True`.

Use one of the following two methods to start the dockers. Once the dockers are up and running, we can run the client same as part1. The client will send requests and get responses from the servers.

### 1. Manually building and running the dockers:

The `build.sh` file contains the commands to build and run the docker containers. You can build the each docker file individually by running thier respective build and run commands (can be found in build.sh file) or just run the build file using the following command from the root directory:
```
bash build.sh
```
This will build the docker containers and start them.

Note:
One important thing to check while running the above script is that the environment variables `CATALOG_HOST`, `ORDER_HOST` should be set to correct IP addresses of catalog and order servers. In the build file they are set to default values (from our observation these are the IP addresses created for them everytime the containers are started). If this is not the case, simply comment the 'docker run' commands in the build file and then manually run the commands with the correct IP addresses.
&nbsp;
### 2. Using docker-compose:

Make sure that the config parameter `mode_docker` is set True. We have created a 'docker-compose.yml' file to run the application using docker-compose.

Run the following docker-compose command from the root directory:
```
docker-compose up --build
```

The containers will be up and running and the servers can serve the client requests. To stop and remove the docker containers run the following command:
```
docker-compose down
```

&nbsp;
## Part 3: Testing and Performance Evaluation

Performance tests were run on the application and the graphs and observations are shared in the evaluation document and output document. docs folder also contains design document which gives information about design choices. The test folder contains three files one for each service, which contains the test cases to test that particular service.

&nbsp;
## Division of Work
### Vineeth:
* Implemented Catalog Service
* Implemented Order Service
* Co-implemented Client
* Wrote test cases for Frontend service
* Worked on docker and virtualization
* Performed evaluation and updating Readme

### Om:
* Implemented Frontend service
* Implemented Proto
* Co-implemented Client
* Wrote test cases for Catalog and Order service
* Worked on docker and virtualization
* Wrote design document and updating ReadMe
