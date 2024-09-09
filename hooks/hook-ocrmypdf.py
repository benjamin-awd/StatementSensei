# pylint: disable=invalid-name
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
    copy_metadata,
)

datas = copy_metadata("pikepdf") + copy_metadata("ocrmypdf")
datas += collect_data_files("ocrmypdf")
hiddenimports = collect_submodules("ocrmypdf")
