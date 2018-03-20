FROM ubuntu
EXPOSE 8080

RUN apt-get clean && \
    apt-get -y update &&\
    apt-get -y install gcc ca-certificates gettext-base poppler-utils swig python-dev

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
RUN python -m spacy download en

COPY . /usr/src/app

CMD python server.py
