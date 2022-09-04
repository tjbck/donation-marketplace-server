# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ENV SECRET_KEY="SECRET_KEY"
ENV RECAPTCHA_SECRET="RECAPTCHA_SECRET"

ENV DB_CRED="root:root"
ENV DB_URL="localhost:27017"
ENV ENV=prod



WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .


RUN pytest

CMD [ "sh", "start.sh"]
