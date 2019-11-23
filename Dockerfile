
FROM python:3.7

MAINTAINER robelkebede44@gmail.com


WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt  

COPY . /app

#RUN python sqlite_database_for_bota.py

EXPOSE 8080

CMD ["python","new_server.py"]



