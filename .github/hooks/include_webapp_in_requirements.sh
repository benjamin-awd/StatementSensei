#!/bin/sh

REQUIREMENTS_FILE="requirements.txt"
VERSION=$(poetry version --short)
TAR_FILE="dist/statement_sensei-$VERSION.tar.gz"

poetry export -f requirements.txt --output requirements.txt --extras ocrmypdf --without dev

if [ -f "$REQUIREMENTS_FILE" ]; then
    FIRST_LINE=$(head -n 1 "$REQUIREMENTS_FILE")
    if [ "$FIRST_LINE" != "$TAR_FILE" ]; then
        echo "Adding $TAR_FILE to the top of $REQUIREMENTS_FILE"
        (echo "$TAR_FILE" && cat "$REQUIREMENTS_FILE") > "$REQUIREMENTS_FILE.tmp"
        mv "$REQUIREMENTS_FILE.tmp" "$REQUIREMENTS_FILE"
    fi
else
    echo "$REQUIREMENTS_FILE does not exist."
fi
