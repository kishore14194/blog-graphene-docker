FROM python:3.6-alpine
MAINTAINER Kishore

ENV PYTHONUNBUFFERED 1
COPY ./requirement.txt /requirement.txt
RUN pip install -r requirement.txt

RUN mkdir /app
WORKDIR /app
COPY ./blog_reconsys /app

RUN adduser -D user
USER user
