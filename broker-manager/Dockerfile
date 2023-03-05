# FROM tiangolo/uvicorn-gunicorn-fastapi
FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN pip3 install --upgrade pip

COPY ./requirements.txt .

RUN pip3 install -r ./requirements.txt

COPY ./app /app

WORKDIR /app


