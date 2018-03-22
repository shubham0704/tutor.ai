FROM python:2.7-slim
EXPOSE 8080

RUN apt-get -y update &&\
    apt-get -y install poppler-utils swig python-dev build-essential libpulse-dev

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install pip==9.0.1
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
RUN python -m spacy download en

COPY . /usr/src/app

CMD python server.py
