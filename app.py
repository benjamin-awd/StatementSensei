from tempfile import NamedTemporaryFile

import streamlit as st
import pandas as pd
from monopoly.processors import detect_processor, UnsupportedBankError
from monopoly.pdf import WrongPasswordError, MissingPasswordError
from pydantic import SecretStr


def parse_bank_statement(file_path: str, password: str = None):
    processor = detect_processor(file_path, [SecretStr(password)])
    statement = processor.extract()
    df = processor.transform(statement)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
    df.columns = ["Transaction Date", "Description", "Amount"]
    st.dataframe(df, use_container_width=True, hide_index=True)

st.set_page_config(page_title="Monopoly", layout="wide")

st.image("./logo.svg", width=400)

st.markdown("Convert bank statements to CSV")

uploaded_file = st.file_uploader("Upload a bank statement", type="pdf")

if uploaded_file:
    try:
        with NamedTemporaryFile(dir=".", suffix=".pdf") as file:
            file.write(uploaded_file.read())
            parse_bank_statement(file.name)
    except MissingPasswordError:
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
                try:
                    with NamedTemporaryFile(dir=".", suffix=".pdf") as file:
                        file.write(uploaded_file.getbuffer())
                        parse_bank_statement(file.name, password)
                except WrongPasswordError:
                    st.error("Wrong password. Please try again.")

    except UnsupportedBankError:
        st.error("This bank is not currently supported")
