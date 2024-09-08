# pylint: disable=unsubscriptable-object
from typing import Optional

import pandas as pd
import streamlit as st
from monopoly.banks import BankDetector, banks
from monopoly.generic import GenericBank
from monopoly.pdf import PdfDocument, PdfParser
from monopoly.pipeline import Pipeline
from monopoly.statements.base import SafetyCheckError
from pydantic import SecretStr

from webapp.models import Config, ProcessedFile, TransactionMetadata


def parse_bank_statement(
    document: PdfDocument, password: Optional[str] = None
) -> ProcessedFile:
    analyzer = BankDetector(document)
    bank = analyzer.detect_bank(banks) or GenericBank
    parser = PdfParser(bank, document)

    if parser.ocr_available:
        with st.spinner(f"Adding OCR layer for {document.name}"):
            # certain PDFs have strange formats that can break the OCR,
            # so they need to be cropped before further processing
            if cropbox := bank.pdf_config.page_bbox:
                for page in parser.document:
                    page.set_cropbox(cropbox)

            parser.document = parser.apply_ocr(document)

    pipeline = Pipeline(parser, passwords=[SecretStr(password)])

    # skip initial safety check, and handle it outside the pipeline
    # so that we can raise a warning and still show transactions
    statement = pipeline.extract(safety_check=False)
    bank_name = parser.bank.__name__

    if statement.config.safety_check:
        try:
            statement.perform_safety_check()
        except SafetyCheckError:
            st.error(
                f"Safety check failed for {document.name}, transactions are incorrect or missing",
                icon="❗",
            )

    if bank_name == "GenericBank":
        st.warning("Unrecognized bank - using generic parser", icon="⚠️")

    metadata = TransactionMetadata(bank_name)
    processed_file = ProcessedFile(pipeline.transform(statement), metadata)

    return processed_file


def create_df(processed_files: list[ProcessedFile], config: Config) -> pd.DataFrame:
    dataframes = []
    for file in processed_files:
        df = pd.DataFrame(file)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        if config.show_banks:
            df["bank"] = file.metadata.bank_name

        df = df.drop(columns="suffix")
        total_balance = df["amount"].sum()

        # reorder and title case columns
        desired_order = ["date", "description", "amount", "bank"]
        columns_to_use = [col for col in desired_order if col in df.columns]
        df = df[columns_to_use]
        df.columns = [col.title() for col in df.columns]
        dataframes.append(df)

    concat_df = pd.concat(dataframes)
    st.dataframe(
        concat_df.style.format({"Amount": "{:.2f}"}),
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
