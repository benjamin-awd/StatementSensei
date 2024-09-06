import pandas as pd
import streamlit as st
from monopoly.pdf import PdfDocument, WrongPasswordError
from monopoly.statements import Transaction
from pymupdf import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

from webapp.constants import APP_DESCRIPTION
from webapp.helpers import create_df, parse_bank_statement
from webapp.logo import logo
from webapp.models import Config


def app() -> pd.DataFrame:
    st.set_page_config(page_title="Statement Sensei", layout="wide")
    st.image(logo, width=450)
    st.markdown(APP_DESCRIPTION)

    with st.sidebar.expander("Config"):
        show_banks = st.toggle("Include bank name")

    config = Config(show_banks)
    files = get_files()

    df = None
    if files:
        transactions = process_files(files)
        df = create_df(transactions, config)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            mime="text/csv",
        )

    return df


@st.cache_data(show_spinner=False)
def handle_file(file_bytes, file_name) -> pd.DataFrame | None:
    document = PdfDocument(file_bytes=file_bytes)
    document._name = file_name

    if document.is_encrypted:  # pylint: disable=no-member
        return handle_encrypted_document(document)

    return parse_bank_statement(document)


def handle_encrypted_document(document: Document) -> None:
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
            return parse_bank_statement(document, password=password)
        except (ValueError, WrongPasswordError):
            st.error("Wrong password. Please try again.")
            return None
    else:
        st.error("Failed to decrypt the document.")
        return None


def process_files(files: list[UploadedFile]) -> list[Transaction] | None:
    num_files = len(files)
    show_pbar = num_files > 4

    pbar = st.progress(0, text="Processing PDFs") if show_pbar else None

    all_transactions = []
    for i, file in enumerate(files):
        if pbar:
            pbar.progress(i / num_files, text=f"Processing {file.name}")

        file_bytes = file.getvalue()
        transactions = handle_file(file_bytes, file.name)
        if transactions:
            all_transactions.extend(transactions)

    if pbar:
        pbar.empty()

    return transactions


def get_files() -> list[UploadedFile]:
    return st.file_uploader(
        label="Upload a bank statement",
        type="pdf",
        label_visibility="hidden",
        accept_multiple_files=True,
    )


if __name__ == "__main__":
    app()
