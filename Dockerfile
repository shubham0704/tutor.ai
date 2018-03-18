FROM python:2.7-slim 
EXPOSE 8080

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD python server.py
