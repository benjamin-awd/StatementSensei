FROM python:3.12-slim AS base

# Install system dependencies for pdftotext
RUN apt-get update && \
    apt-get -y install build-essential libpoppler-cpp-dev pkg-config ocrmypdf \
    # uv build dependencies
    curl git

# Install uv (official binary)
# Download the latest installer
ADD https://astral.sh/uv/0.7.8/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

ENV UV_CACHE_DIR=/tmp/uv-cache \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

COPY pyproject.toml README.md entrypoint.py ./
COPY webapp/ ./webapp

# Install Python dependencies
RUN --mount=type=cache,target=$UV_CACHE_DIR \
uv venv && uv sync --all-extras --group build

CMD ["uv", "run", "entrypoint.py"]
