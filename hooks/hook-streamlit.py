# pylint: disable=invalid-name
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
    copy_metadata,
)

datas = copy_metadata("streamlit")
datas += collect_data_files("streamlit")
hiddenimports = collect_submodules("streamlit")
