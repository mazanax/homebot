FROM python:3.10-slim

ENV PATH=/root/.poetry/bin:${PATH} \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN \
    apt-get update \
    && pip install -U pip \
    && pip install pipenv \
    && pip install "poetry==$POETRY_VERSION" \
    && rm -rf /var/lib/apt/lists

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY main.py tasks.py ./
