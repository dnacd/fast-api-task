FROM python:3.9
LABEL MAINTAINER="Pixelfield, s.r.o"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY ./scripts /scripts
WORKDIR /app

# RUN mkdir /app
COPY ./app /app
ENV PYTHONPATH=/app
