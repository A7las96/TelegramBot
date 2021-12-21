# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

RUN pip3 install aiogram imagehash pillow
CMD ['main.py']
COPY . .

