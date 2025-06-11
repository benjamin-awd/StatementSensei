# pylint: disable=unsubscriptable-object

import pandas as pd
import streamlit as st
from monopoly.banks import BankDetector, banks
from monopoly.generic import GenericBank
from monopoly.pdf import MissingOCRError, PdfDocument, PdfParser
from monopoly.pipeline import Pipeline
from monopoly.statements.base import SafetyCheckError
from pydantic import SecretStr

from webapp.models import ProcessedFile, TransactionMetadata


def build_pipeline(document: PdfDocument, password: str | None = None) -> tuple[Pipeline, PdfParser]:
    analyzer = BankDetector(document)
    bank = analyzer.detect_bank(banks) or GenericBank
    parser = PdfParser(bank, document)
    pipeline = Pipeline(parser, passwords=[SecretStr(password)])
    return pipeline, parser


def parse_bank_statement(document: PdfDocument, password: str | None = None) -> ProcessedFile:
    try:
        pipeline, parser = build_pipeline(document, password)
    except MissingOCRError:
        st.info(f"No text found - {document.name}. Attempting to apply OCR.")
        with st.spinner(f"Adding OCR layer for {document.name}"):
            analyzer = BankDetector(document)
            bank = analyzer.detect_bank(banks) or GenericBank
            # certain PDFs have strange formats that can break the OCR,
            # so they need to be cropped before further processing
            if cropbox := bank.pdf_config.page_bbox:
                for page in document:
                    page.set_cropbox(cropbox)

            document = PdfParser.apply_ocr(document)
            pipeline, parser = build_pipeline(document, password)

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
    if not statement.config.safety_check:
        st.warning(
            f"{bank_name} {statement.config.statement_type} statements have no safety check, "
            "please review your transactions and proceed with caution",
            icon="⚠️",
        )

    if bank_name == "GenericBank":
        st.warning("Unrecognized bank - using generic parser", icon="⚠️")

    metadata = TransactionMetadata(bank_name)
    return ProcessedFile(pipeline.transform(statement), metadata)


def create_df(processed_files: list[ProcessedFile]) -> pd.DataFrame:
    dataframes = []
    for file in processed_files:
        df = pd.DataFrame(file)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["bank"] = file.metadata.bank_name

        df = df.drop(columns="polarity")
        dataframes.append(df)

    concat_df = pd.concat(dataframes)
    st.session_state["df"] = concat_df
    return concat_df


def show_df(df: pd.DataFrame) -> None:
    desired_order = ["date", "description", "amount", "bank"]
    columns_to_use = [col for col in desired_order if col in df.columns]
    df = df[columns_to_use]
    df.columns = [col.title() for col in df.columns]
    st.dataframe(
        df.style.format({"Amount": "{:,.2f}"}),
        use_container_width=True,
        hide_index=True,
    )
    total_balance = df["Amount"].sum()
    st.write(f"Total Balance: ${total_balance:,.2f}")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        mime="text/csv",
    )
