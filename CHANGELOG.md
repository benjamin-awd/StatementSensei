# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2024-06-23

### ⛰️ Features

- Create pyinstaller + tauri app

### 🚜 Refactor

- Move streamlit app logic to monopoly_streamlit dir
- *(streamlit)* Generate app version offline
- *(streamlit)* Add support for logo dark mode
- *(tauri)* Make response loop tighter

### 📚 Documentation

- *(README)* Add about, installation, usage

### ⚙️ Miscellaneous Tasks

- *(streamlit)* Disable telemetry, add viewer mode
- Add pre-commit hook for cargo fmt

## [0.2.0] - 2024-06-22

### ⛰️ Features

- Add streamlit app
- Improve password handling
- Use specific exceptions for password handling
- Improve UI for dataframe
- Add logo
- Add `about` page
- Add total balance
- Store data in memory instead of persisting to disk
- Add download button
- Add linting & pre-commit hooks
- Add version number to release page
- Add support for multiple files
- Provide support for python 3.10

### 🛠️ Bug Fixes

- Use non reserved attribute for document file name
- Contact page badges
- *(build)* Remove mypy from main dependencies

### 🚜 Refactor

- Use formatted column names for dataframe
- Use .read() instead of getbuffer
- Update to monopoly-core
- *(cli)* Remove darwin from release workflow
- *(ci)* Only build app when tags are pushed
- *(build)* Use pake instead of nativefier

### 📚 Documentation

- Add FAQ
- Update about

### ⚙️ Miscellaneous Tasks

- Add badges to contact
- Add currency type to amount col name
- Fix wrong license
- Update README with release information
- Bump monopoly-core to 0.9.4
- Add gitignore

### Build

- *(dev-deps)* Add git cliff
