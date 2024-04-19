from tempfile import NamedTemporaryFile

import streamlit as st
from monopoly.processors import detect_processor
from pydantic import SecretStr


def parse_bank_statement(file_path: str, password: str = None):
    processor = detect_processor(file_path, [SecretStr(password)])
    statement = processor.extract()
    transformed_df = processor.transform(statement)
    st.dataframe(transformed_df, use_container_width=True)


uploaded_file = st.file_uploader("Choose a .pdf file", type="pdf")
if uploaded_file is not None:
    with NamedTemporaryFile(dir=".", suffix=".pdf") as file:
        file.write(uploaded_file.getbuffer())

        try:
            parse_bank_statement(file.name)

        except ValueError:
            password = st.text_input(
                label="password",
                type="password",
                placeholder="Password",
                key="widget",
                label_visibility="hidden",
            )
            if not password:
                st.stop()
            parse_bank_statement(file.name, password)
