FROM ubuntu:latest


RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y mongodb
RUN pip install setuptools


RUN mkdir /data
RUN mkdir /data/db
RUN mkdir /data/log
RUN mongod --fork --logpath /data/log/mongod.log
RUN mkdir /app


WORKDIR /app


COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=pfmtodo.py
ENV FLASK_DEBUG=1


CMD ./startapp.sh

# docker build -t pfmtodo-app .
# docker run -d -p 5000:5000 -v C:/Users/Jeremy/Dev/pfmTodo:/app --name pfmtodo-server pfmtodo-app

