# Changelog

## [0.9.2] - 2025-06-01

### Build

- *(deps)* Update monopoly-core to 0.16.0
- *(deps)* Pin ocrmypdf to 16.10.2
- Use poetry to install pdftotext
- *(deps)* Pin pdftotext to v3.0.0
- *(deps)* Bump streamlit to 1.43.2
- *(deps)* Bump monopoly-core to 0.14.2

### ⚙️ Miscellaneous Tasks

- Attempt hotfix for pdftotext

## [0.9.0] - 2025-01-15

### 🚜 Refactor

- Store password in state and re-use

### 📚 Documentation

- Add Trust to supported banks

### Build

- *(deps)* Bump monopoly-core to 0.14.1

## [0.8.2] - 2025-01-15

### Build

- *(deps)* Bump monopoly-core to 0.14.1

### 🚜 Refactor

- Store password in state and re-use

### 📚 Documentation

- Add Trust to supported banks

### Build

- *(deps)* Bump monopoly-core to 0.14.1

## [0.8.1] - 2024-11-15

### ⚙️ Miscellaneous Tasks

- Improve warning for missing safety check

### Build

- *(deps)* Bump monopoly-core to 0.13.3
- *(deps)* Bump monopoly-core to 0.13.4

## [0.8.0] - 2024-11-15

### 🛠️ Bug Fixes

- *(build)* Add hash to statementsensei tar.gz

### ⚙️ Miscellaneous Tasks

- Add 0.7.4 tar file
- *(ci)* Add stale action
- *(ci)* Add exempt labels for stale action
- *(helpers)* Add warning for statements without statement check

### Build

- *(deps)* Bump monopoly-core to 0.13.2

## [0.7.4] - 2024-10-05

### ⛰️ Features

- *(ci)* Add support for linux/arm64

### 📚 Documentation

- *(README)* Update installation instructions
- *(README)* Add updated instructions for docker

### Build

- Put local tar file in requirements

## [0.7.3] - 2024-09-25

### ⛰️ Features

- Add support for custom server address

### Build

- *(deps)* Bump monopoly-core to 0.12.5

## [0.7.2] - 2024-09-15

### ⚙️ Miscellaneous Tasks

- Allow pushing to docker hub using custom branch

### Build

- *(deps)* Bump monopoly-core to 0.12.4

## [0.7.1] - 2024-09-15

### ⚙️ Miscellaneous Tasks

- Skip release step for development branch

### Build

- *(tauri)* Switch to .deb instead of .appimage
- *(deps)* Bump monopoly-core to 0.12.3

## [0.7.0] - 2024-09-13

### ⛰️ Features

- *(streamlit)* Add cash flow graph

### 🛠️ Bug Fixes

- *(tauri)* Add pyinstaller hook for ocrmypdf
- Resample using start of month
- Add missing plotly dependency

### 🚜 Refactor

- Show bank name in dataframe by default
- Cache dataframe when moving between pages
- *(visualizations)* Show redirect button if no dataframe found

### 🧪 Testing

- Fix order of columns

### ⚙️ Miscellaneous Tasks

- Rename pages with page numbers
- Wait for cashflow graph to load before showing metrics
- Show ticks for each month

## [0.6.6] - 2024-09-08

### 🚜 Refactor

- Allow safety check to be disabled for specific banks

### Build

- *(deps)* Bump monopoly-core to 0.12.2

## [0.6.5] - 2024-09-08

### 📚 Documentation

- Add UOB to supported bank list
- Add ZKB to supported bank list

### Build

- *(deps)* Bump monopoly-core to 0.12.1

## [0.6.4] - 2024-09-08

### ⛰️ Features

- Add caching for files

### 🛠️ Bug Fixes

- *(ci)* Pre-commit hook should include ocrmypdf extras
- Crop pages before applying OCR

### 📚 Documentation

- *(README)* Add note explaining how to inject pdf passwords

### ⚙️ Miscellaneous Tasks

- Add ghostscript deps to streamlit packages
- Add file name to safety check failure message
- Create symlink to tesseract.cfg in webapp
- Update unrecognized bank message
- *(ocr)* Move apply_ocr outside of `id` condition

### Build

- *(deps)* Pin ocrmypdf at version ^15.4.0
- *(deps)* Use ocrmypdf from debian bookworm
- *(deps)* Bump monopoly-core to 0.12.0

## [0.6.3] - 2024-09-05

### 🛠️ Bug Fixes

- *(tauri)* Avoid installing ocrmypdf on windows

## [0.6.2] - 2024-09-05

### ⚙️ Miscellaneous Tasks

- *(ci)* Update tauri with ocrmypdf dependency

## [0.6.1] - 2024-09-05

### 🛠️ Bug Fixes

- *(docker)* Add missing ocrmypdf dependency

### ⚙️ Miscellaneous Tasks

- Move publish workflow to correct directory

### Build

- *(deps)* Bump monopoly-core to 0.11.0

## [0.6.0] - 2024-09-05

### ⛰️ Features

- Add OCR support for HSBC
- Add progress bar for pdfs
- *(ci)* Add publish to docker hub workflow

### 🧪 Testing

- Check protected files can be bypassed using env var

## [0.5.3] - 2024-08-27

### 🛠️ Bug Fixes

- Use onefile mode for MacOS

### 📚 Documentation

- *(README)* Add banner for security warnings
- *(README)* Add note about docker compose

## [0.5.2] - 2024-08-26

### Build

- *(deps)* Bump monopoly-core to 0.10.10

## [0.5.1] - 2024-08-17

### ⚙️ Miscellaneous Tasks

- Bump monopoly-core to 0.10.8

## [0.5.0] - 2024-08-16

### ⛰️ Features

- Add bank to dataframe
- Add integration test

### 🚜 Refactor

- Move supported banks and app description to constants
- *(ci)* Replace pylint pre-commit with ruff and flake8

### 📚 Documentation

- *(README)* Update gif
- *(README)* Add link to core monopoly library

### Build

- Add Docker support

## [0.4.5] - 2024-08-11

### 📚 Documentation

- *(README)* Update usage/install information

### ⚙️ Miscellaneous Tasks

- Bump monopoly-core to 0.10.7

## [0.4.4] - 2024-08-11

### Build

- *(deps)* Bump monopoly-core to 0.10.6

## [0.4.3] - 2024-07-16

### ⛰️ Features

- *(tauri)* Enable HTML5 drag and drop

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
