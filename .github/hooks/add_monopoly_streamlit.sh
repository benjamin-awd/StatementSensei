#!/bin/sh

REQUIREMENTS_FILE="requirements.txt"
DOT="."

if [ -f "$REQUIREMENTS_FILE" ]; then
    FIRST_LINE=$(head -n 1 "$REQUIREMENTS_FILE")
    if [ "$FIRST_LINE" != "$DOT" ]; then
        echo "Adding '.' to the top of $REQUIREMENTS_FILE"
        (echo "$DOT" && cat "$REQUIREMENTS_FILE") > "$REQUIREMENTS_FILE.tmp"
        mv "$REQUIREMENTS_FILE.tmp" "$REQUIREMENTS_FILE"
    fi
else
    echo "$REQUIREMENTS_FILE does not exist."
fi
