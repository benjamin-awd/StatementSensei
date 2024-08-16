# pylint: disable=no-name-in-module
from unittest.mock import patch
from uuid import uuid4

import pandas as pd
import pytest
from streamlit.proto.Common_pb2 import FileURLs
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

from webapp.app import app


@pytest.fixture
def uploaded_file(file_name="example_statement.pdf"):
    with open(f"tests/fixtures/{file_name}", "rb") as f:
        raw_file = f.read()

    file_id = str(uuid4())

    record = UploadedFileRec(
        file_id=file_id, name=file_name, type="application/pdf", data=raw_file
    )
    upload_url = f"/_stcore/upload_file/{uuid4()}/{file_id}"
    file_urls = FileURLs(upload_url=upload_url, delete_url=upload_url)

    return UploadedFile(record, file_urls)


def test_app(uploaded_file):
    with patch("webapp.app.get_files") as get_files:
        get_files.return_value = [uploaded_file]
        df = app()

    expected_df = pd.read_csv("tests/fixtures/example_statement.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    expected_df["Date"] = pd.to_datetime(expected_df["Date"])

    assert df.equals(expected_df)