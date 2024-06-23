# pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

datas = [("./monopoly_streamlit", "./monopoly_streamlit")]
datas += copy_metadata("monopoly_streamlit")
hiddenimports = collect_submodules("monopoly_streamlit")
