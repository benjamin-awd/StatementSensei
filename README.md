<img src="./docs/logo.svg" width="396" height="91">

Statement Sensei converts bank statement PDFs to CSVs using the [monopoly](https://github.com/benjamin-awd/monopoly) CLI library. The offline version of the app is available on the [releases](https://github.com/benjamin-awd/statementsensei/releases) page.

<h3 align="center">
    🎉 Statement Sensei is now live! 🎉
    <br><br>
    Try it out: <br>
    <a href="https://statementsensei.streamlit.app/">https://statementsensei.streamlit.app/</a>
</h3>

<p align="center">
    <img src="./docs/statement_sensei_demo.gif" width=800>
</p>

# Usage

Statement Sensei can be run as an offline application on Windows, MacOS or Linux.

The offline application runs Streamlit locally, and uses a [WebView](https://tauri.app/v1/references/webview-versions/) window to view the browser frontend at http://localhost:8501.

Currently supported banks:
| Bank                 | Credit Statement   | Debit Statement       |
|----------------------|--------------------|-----------------------|
| Bank of America      | ✅                 | ❌                   |
| Chase                | ✅                 | ❌                   |
| Citibank             | ✅                 | ❌                   |
| DBS/POSB             | ✅                 | ✅                   |
| HSBC                 | ✅                 | ❌                   |
| Maybank              | ✅                 | ✅                   |
| OCBC                 | ✅                 | ✅                   |
| Standard Chartered   | ✅                 | ❌                   |
| Trust                | ✅                 | ❌                   |
| UOB                  | ✅                 | ✅                   |
| Zürcher Kantonalbank | ❌                 | ✅                   |

# Installation

> [!WARNING]
> The offline app may raise security warnings during installation.

Specifically on MacOS, the application will show an "app is damaged and can't be opened" error.

These security warnings happen because the release binaries are unsigned, and are incorrectly flagged as malware.

To get around this, follow these steps for [MacOS](https://support.apple.com/en-sg/guide/mac-help/mh40616/mac) / [Windows](https://stackoverflow.com/questions/54733909/windows-defender-alert-users-from-my-pyinstaller-exe).

The Windows Defender alert can be bypassed by clicking "More info" -> "Run anyway".

# Development
Install system dependencies using brew or apt-get (necessary since `pdftotext` needs them)

```sh
apt-get install build-essential libpoppler-cpp-dev pkg-config ocrmypdf
```

or

```sh
brew install gcc@11 pkg-config poppler ocrmypdf
```

Install app dependencies with uv:
```shell
uv venv
source .venv/bin/activate
uv pip install -e .
```

To run the consumer-facing application:
```shell
python entrypoint.py
```

To run the application in developer mode:
```shell
streamlit run webapp/app.py
```

## Docker
Otherwise, to run the application as a container:
```sh
docker compose up
```

or:

```sh
docker pull benjaminawd/statementsensei:latest
docker run -p 8501:8501 benjaminawd/statementsensei:latest
```

If running locally with docker: you can either store passwords in an environment variable as a string

```sh
export PDF_PASSWORDS='["pass123", "otherpw123"]'
```

or store them in an .env file in the project root:

```sh
echo 'PDF_PASSWORDS=["foo"]' > .env
```

# Features
- Supports uploading multiple bank statements
- Allows unlocking of PDFs using user-provided credentials via the frontend
