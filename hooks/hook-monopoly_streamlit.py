# pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_submodules

datas = [("./monopoly_streamlit", "./monopoly_streamlit")]
hiddenimports = collect_submodules("monopoly_streamlit")
