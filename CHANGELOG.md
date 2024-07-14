# Changelog

## [0.4.2] - 2024-07-14

### ⚙️ Miscellaneous Tasks

- Add example statement

### Build

- *(deps)* Bump monopoly-core to 0.10.3

## [0.4.1] - 2024-07-14

### Build

- *(deps)* Bump monopoly-core to 0.10.2

## [0.4.0] - 2024-07-07

### 🚜 Refactor

- Rename app to StatementSensei

### 📚 Documentation

- *(README)* Add note about installation false postives

## [0.3.5] - 2024-06-29

### 🛠️ Bug Fixes

- *(build)* Use onefile for ubuntu

### 🚜 Refactor

- *(tauri)* Use log crate instead of println
- *(tauri/pyinstaller)* Use onedir instead of single executable

### ⚙️ Miscellaneous Tasks

- Add monopoly-streamlit module to requirements.txt
- Add linting for hooks

### Build

- *(deps)* Add hook to ensure monopoly-streamlit is in requirements

## [0.3.4] - 2024-06-24

### 🛠️ Bug Fixes

- *(streamlit)* Filter out None from list of dfs

### 🚜 Refactor

- *(streamlit)* Raise warning instead of failure if safety check failed

### 📚 Documentation

- *(CHANGELOG)* Remove redundant changelog header line
- Remove old links to monopoly-streamlit repo

### ⚙️ Miscellaneous Tasks

- *(CHANGELOG)* Only include latest changes in release
- Add Optional type hint for password string
- Add type hint for file_name

## [0.3.3] - 2024-06-23

### 🛠️ Bug Fixes

- Use forked pybadges to address jinja2 bug

### 📚 Documentation

- *(README)* Re-order info about offline app
- *(README)* Add list of currently supported banks

## [0.3.2] - 2024-06-23

### 🚜 Refactor

- *(streamlit)* Split up file and password handling

### ⚙️ Miscellaneous Tasks

- *(tauri)* Add publisher
- *(tauri)* Include license

### Build

- *(deps)* Bump streamlit to 1.36.0

## [0.3.1] - 2024-06-23

### ⚙️ Miscellaneous Tasks

- Bump monopoly-core to 0.9.5

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
