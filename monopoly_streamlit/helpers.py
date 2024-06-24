# pylint: disable=unsubscriptable-object
import pandas as pd
import streamlit as st
from monopoly.pipeline import Pipeline
from monopoly.statements.base import SafetyCheckError
from pydantic import SecretStr
from pymupdf import Document


def parse_bank_statement(document: Document, password: str = None) -> pd.DataFrame:
    pipeline = Pipeline(file_bytes=document.tobytes(), passwords=[SecretStr(password)])

    # skip initial safety check, and handle it outside the pipeline
    # so that we can raise a warning and still show transactions
    statement = pipeline.extract(safety_check=False)
    try:
        statement.perform_safety_check()
    except SafetyCheckError:
        st.error(
            "Safety check failed, transactions are incorrect or missing", icon="❗"
        )

    if statement.bank.__name__ == "GenericBank":
        st.warning(
            "This bank is not supported - transactions may be inaccurate", icon="⚠️"
        )

    transactions = pipeline.transform(statement)

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


def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    # pylint: disable=import-outside-toplevel
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("app.py")

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")
