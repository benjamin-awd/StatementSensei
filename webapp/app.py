import pandas as pd
import streamlit as st
from monopoly.pdf import MissingPasswordError, PdfDocument
from streamlit.runtime.uploaded_file_manager import UploadedFile

from webapp.constants import APP_DESCRIPTION
from webapp.helpers import create_df, parse_bank_statement, show_df, show_notices
from webapp.logo import logo
from webapp.models import ProcessedFile

# number of files that need to be added before progress bar appears
PBAR_MIN_FILES = 4


def app() -> pd.DataFrame:
    st.set_page_config(page_title="Statement Sensei", layout="wide")
    st.image(logo, width=450)
    st.markdown(APP_DESCRIPTION)

    files = get_files()

    df = None
    if "df" in st.session_state:
        df = st.session_state["df"]

    if files:
        processed_files = process_files(files)

        if processed_files:
            df = create_df(processed_files)

    if df is not None:
        show_df(df)

    return df


def process_files(uploaded_files: list[UploadedFile]) -> list[ProcessedFile] | None:
    num_files = len(uploaded_files)
    show_pbar = num_files > PBAR_MIN_FILES

    pbar = st.progress(0, text="Processing PDFs") if show_pbar else None

    # cache parsed files by upload id, dropping any that were removed from the uploader
    cache: dict[str, ProcessedFile] = st.session_state.setdefault("processed_files", {})
    current_ids = {file.file_id for file in uploaded_files}
    for file_id in cache.keys() - current_ids:
        del cache[file_id]

    processed_files = []
    for i, file in enumerate(uploaded_files):
        if pbar:
            pbar.progress(i / num_files, text=f"Processing {file.name}")

        if file.file_id not in cache:
            document = open_document(file)
            if document is None:
                continue
            cache[file.file_id] = parse_bank_statement(document)

        processed_file = cache[file.file_id]
        show_notices(processed_file)
        processed_files.append(processed_file)

    if pbar:
        pbar.empty()

    return processed_files


def open_document(file: UploadedFile) -> PdfDocument | None:
    document = PdfDocument(file_bytes=file.getvalue())
    document._name = file.name

    # attempt to use passwords stored in environment to unlock
    # if no passwords in environment, then ask user for password
    if document.is_encrypted:  # pylint: disable=no-member
        try:
            return document.unlock_document()
        except MissingPasswordError:
            return handle_encrypted_document(document)

    return document


def handle_encrypted_document(document: PdfDocument) -> PdfDocument | None:
    passwords: list[str] = st.session_state.setdefault("pdf_passwords", [])

    # Try existing passwords first
    for password in passwords:
        document.authenticate(password)
        if not document.is_encrypted:  # pylint: disable=no-member
            return document

    # Prompt user for password if none of the existing passwords work
    password_container = st.empty()
    password = password_container.text_input(
        label="Password",
        type="password",
        placeholder=f"Enter password for {document.name}",
        key=document.name,
    )

    if not password:
        return None

    document.authenticate(password)

    if not document.is_encrypted:  # pylint: disable=no-member
        passwords.append(password)
        password_container.empty()
        return document

    st.error("Wrong password. Please try again.")
    return None


def get_files() -> list[UploadedFile]:
    return st.file_uploader(
        label="Upload a bank statement",
        type="pdf",
        label_visibility="hidden",
        accept_multiple_files=True,
    )


if __name__ == "__main__":
    app()
