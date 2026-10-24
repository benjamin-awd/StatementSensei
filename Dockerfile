FROM python:3.12-slim-trixie AS builder

# build dependencies for pdftotext, plus git for the pybadges git dependency
RUN apt-get update && \
    apt-get -y install --no-install-recommends build-essential libpoppler-cpp-dev pkg-config git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /bin/uv

ENV UV_CACHE_DIR=/tmp/uv-cache \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    VIRTUAL_ENV=/opt/venv

WORKDIR /app

# requirements.txt pins every dependency; install those first so the layer is
# reused when only the app code changes, then install the app itself
COPY requirements.txt ./
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv venv "$VIRTUAL_ENV" && \
    grep -vx '\.' requirements.txt > /tmp/deps.txt && \
    uv pip install -r /tmp/deps.txt

COPY pyproject.toml README.md ./
COPY webapp/ ./webapp
RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv pip install --no-deps .


FROM python:3.12-slim-trixie

# runtime libraries for pdftotext and ocrmypdf
RUN apt-get update && \
    apt-get -y install --no-install-recommends libpoppler-cpp2 tesseract-ocr ghostscript && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY .streamlit/ ./.streamlit
COPY entrypoint.py tesseract.cfg ./
COPY webapp/ ./webapp

EXPOSE 8501

CMD ["python", "entrypoint.py"]
