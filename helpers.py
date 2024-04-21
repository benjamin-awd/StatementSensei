import pandas as pd
import streamlit as st
from pydantic import SecretStr

from monopoly.processors import detect_processor


def parse_bank_statement(file_bytes: bytes, password: str = None) -> None:
    processor = detect_processor(file_bytes=file_bytes, passwords=[SecretStr(password)])
    statement = processor.extract()
    df = processor.transform(statement)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
    df.columns = ["Transaction Date", "Description", "Amount"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    total_balance = df["Amount"].sum()
    st.write(f"Total Balance: ${total_balance:.2f}")
