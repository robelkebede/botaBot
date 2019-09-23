
FROM ubuntu:16.04


MAINTAINER robelkebede44@gmail.com


# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 68818C72E52529D4


RUN echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" |` tee /etc/apt/sources.list.d/mongodb-org-4.0.list


RUN apt-get update

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
EXPOSE 8000

RUN "python new_server.py"



