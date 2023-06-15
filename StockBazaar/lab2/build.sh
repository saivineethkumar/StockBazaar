#!/bin/bash

# command to build the frontend server
docker build -f frontend.Dockerfile -t frontend .

# command to build the catalog server
docker build -f catalog.Dockerfile -t catalog .

# command to build the order server
docker build -f order.Dockerfile -t order .


# NOTE: uncomment the following 'docker run' lines if the bash file just needs to build the dockers and not run them
# Keep a note of the environment variables mentioned in the commands, here they are set to default values based on our observations.
# If the IP addresses are different from these please modify them according to the below comments and run them or simply use docker-compose 


# command to run the catalog docker container 
docker run -d --name my_catalog --env CATALOG_HOST=0.0.0.0 --volume `pwd`/src/backend/catalog/data:/src/backend/catalog/data -p 26119:26119 catalog

# command to run the order docker container
# CATALOG_HOST env variable contains the ip address of catalog server that was run using the above command
docker run -d --name my_order --env CATALOG_HOST=172.17.0.2 --env ORDER_HOST=0.0.0.0 --volume `pwd`/src/backend/order/data:/src/backend/order/data -p 26117:26117 order

# command to run the frontend docker container
# ORDER_HOST, CATALOG_HOST env variables contains the ip address of order server and catalog servers that were run using the above commands
docker run -d --name my_frontend --env CATALOG_HOST=172.17.0.2 --env ORDER_HOST=172.17.0.3 -p 26111:26111 frontend


# Note:
# Instead all the above commands, we can simply use docker-compose command to build and start the containers.
# Comment all the above lines of code and uncomment the below line to build and run the containers using the docker-compose command
# docker-compose up --build