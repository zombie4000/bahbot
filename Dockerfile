FROM python:3-alpine

LABEL author="dracz"
LABEL version="1.1.5"

COPY ./app /app

WORKDIR /app

RUN apk update && apk add --no-cache --virtual .build-deps build-base && \
pip install --no-cache-dir discord.py && \
apk del .build-deps

ENV TOKEN="token"

ENTRYPOINT python bahbot.py -t $TOKEN