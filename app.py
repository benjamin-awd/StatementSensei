from tempfile import NamedTemporaryFile

import streamlit as st
from uuid import uuid4
from monopoly.processors import detect_processor
from pydantic import SecretStr


def parse_bank_statement(file_path: str, password: str = None):
    processor = detect_processor(file_path, [SecretStr(password)])
    statement = processor.extract()
    transformed_df = processor.transform(statement)
    st.dataframe(transformed_df, use_container_width=True)

uploaded_file = st.file_uploader("Choose a .pdf file", type="pdf")

if uploaded_file:
    try:
        with NamedTemporaryFile(dir=".", suffix=".pdf") as file:
            file.write(uploaded_file.getbuffer())
            parse_bank_statement(file.name)
    except ValueError:
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
                except ValueError:
                    st.error("Wrong password. Please try again.")
