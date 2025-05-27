#!/bin/sh

REQUIREMENTS_FILE="requirements.txt"
VERSION=$(poetry version --short)
TAR_FILE="dist/statement_sensei-$VERSION.tar.gz"
HASH=$(sha256sum "$TAR_FILE" | awk '{ print $1 }')

uv export --output-file requirements.txt --all-extras

if [ -f "$REQUIREMENTS_FILE" ]; then
    FIRST_LINE=$(head -n 1 "$REQUIREMENTS_FILE")
    # Create the required entry with hash
    TAR_WITH_HASH="dist/statement_sensei-$VERSION.tar.gz --hash=sha256:$HASH"

    if [ "$FIRST_LINE" != "$TAR_WITH_HASH" ]; then
        echo "Adding $TAR_WITH_HASH to the top of $REQUIREMENTS_FILE"
        (echo "$TAR_WITH_HASH" && cat "$REQUIREMENTS_FILE") > "$REQUIREMENTS_FILE.tmp"
        mv "$REQUIREMENTS_FILE.tmp" "$REQUIREMENTS_FILE"
    fi
else
    echo "$REQUIREMENTS_FILE does not exist."
fi
