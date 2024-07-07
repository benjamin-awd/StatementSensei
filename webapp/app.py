import pandas as pd
import streamlit as st
from monopoly.pdf import WrongPasswordError
from pymupdf import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

from webapp.helpers import format_df, parse_bank_statement
from webapp.logo import logo


def handle_file(file: UploadedFile) -> pd.DataFrame | None:
    file_bytes = file.getvalue()
    document = Document(stream=file_bytes)

    if document.is_encrypted:  # pylint: disable=no-member
        return handle_encrypted_document(document, file.name)

    return parse_bank_statement(document)


def handle_encrypted_document(
    document: Document, file_name: str
) -> pd.DataFrame | None:
    password_container = st.empty()
    password = password_container.text_input(
        label="Password",
        type="password",
        placeholder=f"Enter password for {file_name}",
        key=file_name,
    )

    if not password:
        st.warning("Please enter a password.")
        return None

    document.authenticate(password)

    if not document.is_encrypted:  # pylint: disable=no-member
        password_container.empty()
        try:
            return parse_bank_statement(document, password)
        except (ValueError, WrongPasswordError):
            st.error("Wrong password. Please try again.")
            return None
    else:
        st.error("Failed to decrypt the document.")
        return None


def app() -> None:
    st.set_page_config(page_title="Statement Sensei", layout="wide")
    st.image(logo, width=450)
    st.markdown(
        """
        ## Convert bank statements to CSV
        Effortlessly extract transactions from PDF bank statements.
        """
    )

    uploaded_files = st.file_uploader(
        label="Upload a bank statement",
        type="pdf",
        label_visibility="hidden",
        accept_multiple_files=True,
    )

    dataframes = []
    for file in uploaded_files:
        df = handle_file(file)
        if isinstance(df, pd.DataFrame):
            dataframes.append(df)

    if dataframes:
        concat_df = format_df(pd.concat(dataframes))
        csv = concat_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            mime="text/csv",
        )


if __name__ == "__main__":
    app()
