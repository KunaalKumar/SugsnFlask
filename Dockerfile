from python:3

MAINTAINER kunaal@ashiana.com

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
