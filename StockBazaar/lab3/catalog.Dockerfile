FROM python:3.8-alpine

RUN pip install redis grpcio grpcio-tools

WORKDIR /src

COPY ./src/backend/catalog /src/backend/catalog/
COPY ./src/shared /src/shared
COPY ./src/config.py /src/config.py

# COPY catalog-service.py .

WORKDIR /src/backend/catalog

ENTRYPOINT ["python", "catalog-service.py"]

# command to build and run the catalog docker
# docker build -f catalog.Dockerfile -t catalog . 
# docker run -it --name my_catalog -p 26119:26119 catalog