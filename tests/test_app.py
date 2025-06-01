# pylint: disable=no-name-in-module
import os
from unittest.mock import patch
from uuid import uuid4

import pandas as pd
import pytest
from streamlit.proto.Common_pb2 import FileURLs
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

from webapp.app import app


def create_uploaded_file(file_name):
    with open(f"tests/fixtures/{file_name}", "rb") as f:
        raw_file = f.read()

    file_id = str(uuid4())

    record = UploadedFileRec(file_id=file_id, name=file_name, type="application/pdf", data=raw_file)
    upload_url = f"/_stcore/upload_file/{uuid4()}/{file_id}"
    file_urls = FileURLs(upload_url=upload_url, delete_url=upload_url)

    return UploadedFile(record, file_urls)


@pytest.fixture()
def uploaded_file():
    return create_uploaded_file("example_statement.pdf")


@pytest.fixture()
def protected_file():
    return create_uploaded_file("protected_example_statement.pdf")


def test_app(uploaded_file):
    with patch("webapp.app.get_files") as get_files:
        get_files.return_value = [uploaded_file]
        df = app()

    expected_df = pd.read_csv("tests/fixtures/example_statement.csv")

    df["date"] = pd.to_datetime(df["date"])
    df = df[["description", "amount", "date", "bank"]]
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    assert df.equals(expected_df)


def test_unlock_protected(protected_file):
    os.environ["PDF_PASSWORDS"] = '["foobar123"]'
    with patch("webapp.app.get_files") as get_files:
        get_files.return_value = [protected_file]
        df = app()

    expected_df = pd.read_csv("tests/fixtures/example_statement.csv")

    df["date"] = pd.to_datetime(df["date"])
    df = df[["description", "amount", "date", "bank"]]
    expected_df["date"] = pd.to_datetime(expected_df["date"])

    assert df.equals(expected_df)
