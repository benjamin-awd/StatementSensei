# 💸 Monopoly

**Monopoly** is a Python [library](https://github.com/benjamin-awd/monopoly) and Streamlit application that converts bank statement PDFs to CSVs.

<h3 align="center">
    🎉 Monopoly is now live! 🎉
    <br><br>
    Try it out: <br>
    <a href="https://monopoly.streamlit.app/">https://monopoly.streamlit.app/</a>
</h3>

<p align="center">
    <img src="https://raw.githubusercontent.com/benjamin-awd/monopoly-streamlit/main/docs/streamlit_demo.gif" width=800>
</p>

# Usage

Monopoly is available as a [web application](https://monopoly.streamlit.app), and an offline desktop application that can be downloaded from the [releases](https://github.com/benjamin-awd/monopoly-streamlit/releases) page.

The offline application runs Streamlit locally, and uses a [WebView](https://tauri.app/v1/references/webview-versions/) window to view the browser frontend at http://localhost:8501.

# Development

Install dependencies with Poetry:
```shell
poetry install
poetry shell
```

To run the consumer-facing application:
```shell
python entrypoint.py
```

To run the application in developer mode:
```shell
streamlit run monopoly_streamlit/app.py
```

# Features
- Supports uploading multiple bank statements
- Allows unlocking of PDFs using user-provided credentials via the frontend
