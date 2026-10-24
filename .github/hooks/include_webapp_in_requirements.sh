#!/usr/bin/env bash
# Pin dependencies for Streamlit Community Cloud (and the Docker image), then
# install the app itself from the repo root so its version metadata is available.
set -euo pipefail

REQUIREMENTS_FILE="requirements.txt"

uv export --output-file "$REQUIREMENTS_FILE" --all-extras --no-hashes --no-emit-project --quiet
echo "." >> "$REQUIREMENTS_FILE"
