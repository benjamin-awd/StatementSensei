# pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files("pybadges")
hiddenimports = collect_submodules("pybadges")
