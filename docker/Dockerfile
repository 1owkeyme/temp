FROM python:3.12.2-slim
LABEL maintainer="Vadim Kozyrevskiy" \
      email="v.kozyrevskiy@timeweb.ru"

ENV TZ='Europe/Moscow'

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3-dev git gcc curl && \
    pip install --no-cache-dir --upgrade pip==24.* && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code/src

COPY ./pyproject.toml /code/src/pyproject.toml
RUN pip install --no-cache-dir /code/src/

COPY ./src/ /code/src/
