from python:3

MAINTAINER kunaal@ashiana.com

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
