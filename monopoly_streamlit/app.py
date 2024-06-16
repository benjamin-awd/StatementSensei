import pandas as pd
import streamlit as st
from monopoly.pdf import WrongPasswordError
from pymupdf import Document

from monopoly_streamlit.helpers import format_df, parse_bank_statement
from monopoly_streamlit.logo import logo


def app() -> None:
    st.set_page_config(page_title="Monopoly", layout="wide")

    st.image(logo, width=350)

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
        if file:
            df = None
            file_bytes = file.getvalue()
            document = Document(stream=file_bytes)

            if document.is_encrypted:  # pylint: disable=no-member
                password_container = st.empty()
                password = password_container.text_input(
                    label="Password",
                    type="password",
                    placeholder=f"Enter password for {file.name}",
                    key=file.name,
                )

                if not password:
                    st.warning("Please enter a password.")
                else:
                    document.authenticate(password)

                    # remove the text input box after we're done with it
                    if not document.is_encrypted:  # pylint: disable=no-member
                        password_container.empty()

                    try:
                        df = parse_bank_statement(document, password)

                    except ValueError as err:
                        if err.args[0] == "document closed or encrypted":
                            st.error("Wrong password. Please try again.")

                    except (TypeError, WrongPasswordError):
                        st.error("Wrong password. Please try again.")
            else:
                df = parse_bank_statement(document)

        if df is not None:
            dataframes.append(df)

    if dataframes:
        df = pd.concat(dataframes)
        df = format_df(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            mime="text/csv",
        )


if __name__ == "__main__":
    app()
