# base image
FROM python:3

ENV PYTHONBUFFERED 1
#
#RUN apt-get update \
#   && apt-get -y install netcat gcc \
#   && apt-get clean

WORKDIR /mealhub

RUN pip install --upgrade pip

COPY . /mealhub

COPY ./requirements.txt .

RUN pip install -r requirements.txt
