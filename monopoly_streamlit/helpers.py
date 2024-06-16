# pylint: disable=unsubscriptable-object
import pandas as pd
import streamlit as st
from pymupdf import Document
from monopoly.pipeline import Pipeline
from pydantic import SecretStr


def parse_bank_statement(document: Document, password: str = None) -> pd.DataFrame:
    pipeline = Pipeline(file_bytes=document.tobytes(), passwords=[SecretStr(password)])
    statement = pipeline.extract(safety_check=False)
    transactions = pipeline.transform(statement)

    if statement.bank.__name__ == "GenericBank":
        st.warning(
            "This bank is not supported - transactions may be inaccurate", icon="⚠️"
        )

    df = pd.DataFrame(transactions)
    return df


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.drop(columns="suffix")
    total_balance = df["amount"].sum()

    # cosmetic changes
    df = df[["date", "description", "amount"]]
    df.columns = ["Date", "Description", "Amount"]
    st.dataframe(
        df.style.format({"Amount": "{:.2f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.write(f"Total Balance: ${total_balance:.2f}")
    return df
