FROM python:3.8-alpine

RUN pip install redis grpcio grpcio-tools

WORKDIR /src

COPY ./src/frontend /src/frontend
COPY ./src/shared /src/shared
COPY ./src/config.py /src/config.py

# COPY frontend-service.py .

WORKDIR /src/frontend

ENTRYPOINT ["python", "frontend-service.py"]

# command to build and run the frontend docker
# docker build -f frontend.Dockerfile -t frontend . 
# docker run -it --name my_frontend --env CATALOG_HOST=172.17.0.2 --env ORDER_HOST=172.17.0.3 -p 26111:26111 frontend