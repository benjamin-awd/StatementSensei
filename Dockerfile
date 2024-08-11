FROM python:3.12-slim AS base

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install pdftotext dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get -y install build-essential libpoppler-cpp-dev pkg-config

COPY pyproject.toml poetry.lock README.md entrypoint.py ./
COPY webapp/ ./webapp

# install python dependencies
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev

CMD [ "python", "entrypoint.py" ]
