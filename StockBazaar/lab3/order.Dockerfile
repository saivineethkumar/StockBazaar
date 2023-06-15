FROM python:3.8-alpine

RUN pip install redis grpcio grpcio-tools

WORKDIR /src

COPY ./src/backend/order /src/backend/order/
COPY ./src/shared /src/shared
COPY ./src/config.py /src/config.py

# COPY catalog-service.py .

WORKDIR /src/backend/order

ENTRYPOINT ["python", "order-service.py"]

# command to build and run the order docker
# docker build -f order.Dockerfile -t order . 
# docker run -it --name my_order --env CATALOG_HOST=172.17.0.2 -p 26117:26117 order