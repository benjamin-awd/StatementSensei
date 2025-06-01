import sys
from pathlib import Path

import streamlit.web.cli as stcli
from pydantic_settings import BaseSettings


class StreamlitConfig(BaseSettings):
    browser_server_address: str = "localhost"


def resolve_path(path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", str(Path.cwd()))
    return str(Path(base_path) / path)


if __name__ == "__main__":
    config = StreamlitConfig()
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("webapp/app.py"),
        f"--browser.serverAddress={config.browser_server_address}",
        "--browser.gatherUsageStats=false",
        "--client.toolbarMode=viewer",
        "--global.developmentMode=false",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())
