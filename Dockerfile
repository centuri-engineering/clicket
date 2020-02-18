# from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

FROM python:3.8 as base
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


# pull official base image
FROM python:3.8.1-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
COPY --from=base /wheels /wheels

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
RUN apt-get update && apt-get -y upgrade && apt-get -y install libpq5

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/
