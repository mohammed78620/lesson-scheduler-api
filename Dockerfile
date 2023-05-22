# The base image we want to inherit from
FROM python:3.8

ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV} \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.3.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt update
RUN pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Configure logs folders
RUN mkdir -p /var/log/django/

# Install dependencies:
RUN poetry config virtualenvs.create false
RUN poetry install $(test "$DJANGO_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# copy project
COPY . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]
