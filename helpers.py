import pandas as pd
import streamlit as st
from fitz import Document
from pydantic import SecretStr

from monopoly.processors import detect_processor


def parse_bank_statement(document: Document, password: str = None) -> None:
    processor = detect_processor(file_bytes=document.tobytes(), passwords=[SecretStr(password)])
    statement = processor.extract()
    df = processor.transform(statement)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.date
    df.columns = ["Transaction Date", "Description", "Amount"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    total_balance = df["Amount"].sum()
    st.write(f"Total Balance: ${total_balance:.2f}")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{document.name.split('.')[0]}.csv",
        mime="text/csv"
    )
