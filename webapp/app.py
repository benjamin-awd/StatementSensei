import pandas as pd
import streamlit as st
from monopoly.pdf import PdfDocument, WrongPasswordError
from pymupdf import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

from webapp.constants import APP_DESCRIPTION
from webapp.helpers import Config, format_df, parse_bank_statement
from webapp.logo import logo


def handle_file(file: UploadedFile, config: Config) -> pd.DataFrame | None:
    file_bytes = file.getvalue()
    document = PdfDocument(file_bytes=file_bytes)
    document._name = file.name

    if document.is_encrypted:  # pylint: disable=no-member
        return handle_encrypted_document(document, config)

    return parse_bank_statement(document, config)


def handle_encrypted_document(
    document: Document, config: Config
) -> pd.DataFrame | None:
    password_container = st.empty()
    password = password_container.text_input(
        label="Password",
        type="password",
        placeholder=f"Enter password for {document.name}",
        key=document.name,
    )

    if not password:
        st.warning("Please enter a password.")
        return None

    document.authenticate(password)

    if not document.is_encrypted:  # pylint: disable=no-member
        password_container.empty()
        try:
            return parse_bank_statement(document, config, password=password)
        except (ValueError, WrongPasswordError):
            st.error("Wrong password. Please try again.")
            return None
    else:
        st.error("Failed to decrypt the document.")
        return None


def app() -> pd.DataFrame:
    st.set_page_config(page_title="Statement Sensei", layout="wide")
    st.image(logo, width=450)
    st.markdown(APP_DESCRIPTION)

    with st.sidebar.expander("Config"):
        show_banks = st.toggle("Include bank name")
    config = Config(show_banks)

    uploaded_files = get_files()
    return process_pdf(uploaded_files, config)


def process_pdf(uploaded_files, config) -> pd.DataFrame | None:
    num_files = len(uploaded_files)
    show_pbar = num_files > 4

    pbar = st.progress(0, text="Processing PDFs") if show_pbar else None

    dataframes = []
    for i, file in enumerate(uploaded_files):
        if pbar:
            pbar.progress(i / num_files, text=f"Processing {file.name}")

        df = handle_file(file, config)
        if isinstance(df, pd.DataFrame):
            dataframes.append(df)

    if pbar:
        pbar.empty()

    if dataframes:
        concat_df = format_df(pd.concat(dataframes))
        csv = concat_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            mime="text/csv",
        )
        return concat_df


def get_files() -> list[UploadedFile]:
    return st.file_uploader(
        label="Upload a bank statement",
        type="pdf",
        label_visibility="hidden",
        accept_multiple_files=True,
    )


if __name__ == "__main__":
    app()
