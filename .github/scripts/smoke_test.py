# ruff: noqa: INP001  (standalone CI script, not part of a package)
"""
Smoke test for the deployed Streamlit app.

Checks, in order:
1. (optional) the About page reports ``--expected-version``, polling until it does.
   Streamlit Community Cloud redeploys on its own after a push to main and has no
   deploy API, so the live page is the only signal that a release is served.
2. ``/healthz`` returns 200.
3. The app loads without an error page.
4. Uploading the example statement renders a transactions table.

Streamlit renders pages in the browser over a websocket, so the checks drive a real
browser rather than fetching HTML. Failures are printed as GitHub Actions ``::error::``
annotations and exit non-zero.
"""

import argparse
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import FrameLocator, Page, sync_playwright

DEFAULT_APP_URL = "https://statementsensei.streamlit.app"
EXAMPLE_STATEMENT = Path("docs/example_statement.pdf")
LOAD_TIMEOUT_MS = 60_000
RENDER_WAIT_MS = 5_000
HTTP_OK = 200
VERSION_PATTERN = re.compile(r"Version (\S+)")


class SmokeTestError(Exception):
    """A check failed."""


def log(message: str) -> None:
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def app_root(page: Page) -> Page | FrameLocator:
    """Return the element tree the Streamlit app lives in; Streamlit Cloud wraps it in an iframe."""
    if page.locator("iframe").count():
        return page.frame_locator("iframe").first
    return page


def page_text(page: Page) -> str:
    """Concatenate the visible text of every frame, so wrapped and unwrapped apps read the same."""
    texts = []
    for frame in page.frames:
        try:
            texts.append(frame.locator("body").inner_text())
        except PlaywrightError:
            continue
    return "\n".join(texts)


def wait_for_version(page: Page, app_url: str, expected: str, timeout_minutes: float, poll_seconds: float) -> None:
    deadline = time.monotonic() + timeout_minutes * 60
    seen = "nothing yet"
    while time.monotonic() < deadline:
        try:
            page.goto(f"{app_url}/about", timeout=LOAD_TIMEOUT_MS)
            page.wait_for_timeout(RENDER_WAIT_MS)
            match = VERSION_PATTERN.search(page_text(page))
            seen = match.group(1) if match else "no version on the page"
            if seen == expected:
                log(f"Deployed version is {expected}")
                return
        except PlaywrightError as err:
            seen = f"load error: {str(err).splitlines()[0]}"
        log(f"Waiting for {expected}, saw {seen}")
        time.sleep(poll_seconds)
    msg = f"Version {expected} was not deployed within {timeout_minutes:g} minutes (last saw {seen})"
    raise SmokeTestError(msg)


def check_health(page: Page, app_url: str) -> None:
    response = page.request.get(f"{app_url}/healthz", timeout=LOAD_TIMEOUT_MS)
    if response.status != HTTP_OK:
        msg = f"Health check failed with status {response.status}"
        raise SmokeTestError(msg)
    log(f"Health check passed (HTTP {response.status})")


def check_app_loads(page: Page, app_url: str) -> None:
    page.goto(f"{app_url}/", timeout=LOAD_TIMEOUT_MS)
    page.wait_for_timeout(RENDER_WAIT_MS)
    body = page.locator("body").inner_text()
    if "Error" in body:
        raise SmokeTestError(body.strip())
    log("App loads successfully")


def check_statement_processes(page: Page) -> None:
    root = app_root(page)
    file_input = root.locator('[data-testid="stFileUploader"] input[type="file"]')
    file_input.wait_for(state="attached", timeout=LOAD_TIMEOUT_MS)
    file_input.set_input_files(EXAMPLE_STATEMENT)
    log("Uploaded example statement")

    root.locator('[data-testid="stDataFrame"], table').first.wait_for(state="visible", timeout=LOAD_TIMEOUT_MS)
    log("Statement processed successfully")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--app-url", default=DEFAULT_APP_URL)
    parser.add_argument("--expected-version", default="", help='wait for this version first, e.g. "v0.10.6"')
    parser.add_argument("--version-timeout-minutes", type=float, default=20)
    parser.add_argument("--poll-seconds", type=float, default=30)
    args = parser.parse_args()

    app_url = args.app_url.rstrip("/")
    expected = args.expected_version.removeprefix("v")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        try:
            if expected:
                wait_for_version(page, app_url, expected, args.version_timeout_minutes, args.poll_seconds)
            check_health(page, app_url)
            check_app_loads(page, app_url)
            check_statement_processes(page)
        except (SmokeTestError, PlaywrightError) as err:
            log(f"::error::{err}")
            return 1
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
