from python:3

MAINTAINER kunaal@ashiana.com

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

#CMD git pull
CMD python app.py

EXPOSE 5000
