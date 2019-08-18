from python:3

MAINTAINER kunaal@ashiana.com

WORKDIR /usr/src/app

COPY ./app .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

EXPOSE 5000
