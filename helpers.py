# pylint: disable=unsubscriptable-object
from typing import Type

import pandas as pd
import streamlit as st
from fitz import Document
from monopoly.pipeline import Pipeline
from monopoly.statements import BaseStatement
from pydantic import SecretStr


def parse_bank_statement(
    document: Document, password: str = None
) -> Type[BaseStatement]:
    file_name = f"{document.pdf_file_name.split('.')[0]}.csv"
    pipeline = Pipeline(file_bytes=document.tobytes(), passwords=[SecretStr(password)])
    statement = pipeline.extract(safety_check=False)
    transactions = pipeline.transform(statement)

    if statement.bank.__name__ == "GenericBank":
        st.warning(
            "This bank is not supported - transactions may be inaccurate", icon="⚠️"
        )

    show_dataframe(transactions, file_name)
    return statement


def show_dataframe(transactions: list, file_name: str) -> None:
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.drop(columns="suffix")
    total_balance = df["amount"].sum()

    # cosmetic changes
    df = df[["date", "description", "amount"]]
    df.columns = ["Date", "Description", "Amount ($)"]
    st.dataframe(
        df.style.format({"Amount ($)": "{:.2f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.write(f"Total Balance: ${total_balance:.2f}")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv",
    )
