FROM python:3.12-alpine

LABEL maintainer="blog-app"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG DEV=false

COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

RUN apk add --update --no-cache \
        gcc libpq-dev postgresql-client jpeg-dev \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [$DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi \
    && rm -rf /tmp \
    && apk del gcc libpq-dev

ENV PATH="/py/bin:$PATH"

RUN adduser --disabled-password --no-create-home django-user
USER django-user

EXPOSE 8000