import fitz
import streamlit as st
from monopoly.pdf import WrongPasswordError
from monopoly.processors import UnsupportedBankError

from helpers import parse_bank_statement

st.set_page_config(page_title="Monopoly", layout="wide")

st.image("./logo.svg", width=350)

st.markdown(
    """## Convert bank statements to CSV
Effortlessly extract transactions from PDF bank statements.
"""
)

uploaded_file = st.file_uploader(
    label="Upload a bank statement", type="pdf", label_visibility="hidden"
)

if uploaded_file:
    file_bytes = uploaded_file.read()
    document = fitz.Document(stream=file_bytes)
    document.name = uploaded_file.name

    if document.is_encrypted:  # pylint: disable=no-member
        password = st.text_input(
            label="Password",
            type="password",
            placeholder="Enter password",
        )

        submit_button = st.button("Submit")

        if submit_button:
            if not password:
                st.warning("Please enter a password.")
            else:
                document.authenticate(password)
                try:
                    parse_bank_statement(document, password)

                except ValueError as err:
                    if err.args[0] == "document closed or encrypted":
                        st.error("Wrong password. Please try again.")

                except (TypeError, WrongPasswordError):
                    st.error("Wrong password. Please try again.")

                except UnsupportedBankError:
                    st.error("This bank is not currently supported")
    else:
        try:
            parse_bank_statement(document)
        except UnsupportedBankError:
            st.error("This bank is not currently supported")
