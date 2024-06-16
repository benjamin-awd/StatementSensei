import os
import sys
from pathlib import Path

import monopoly
import pymupdf
import streamlit.web.cli as stcli

import monopoly_streamlit

# this tells pyinstaller to run the hooks
# associated with these packages, making them
# available during the streamlit runtime
__all__ = ["pymupdf", "monopoly", "monopoly_streamlit"]


def resolve_path(path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.getcwd())
    return str(Path(base_path) / path)


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("monopoly_streamlit/app.py"),
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
