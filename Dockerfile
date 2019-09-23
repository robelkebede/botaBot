
FROM ubuntu:16.04


MAINTAINER robelkebede44@gmail.com



# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db



RUN apt-get -y update \
  && apt-get install -y --allow-unauthenticated mongodb-org \
  && apt-get install -y git vim wget python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get clean


WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt  

COPY . /app

#expose every port in the server

EXPOSE *

RUN chmod +x ./start.sh

CMD ["./start.sh"]


