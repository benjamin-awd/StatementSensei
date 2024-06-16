import site
from PyInstaller.utils.hooks import copy_metadata, collect_submodules
from PyInstaller.utils.hooks import collect_data_files

site_packages_dir = site.getsitepackages()[0]
datas = [(f"{site_packages_dir}/streamlit/runtime", "./streamlit/runtime")]
datas = copy_metadata("streamlit")
datas += collect_data_files("streamlit")
hiddenimports = collect_submodules("streamlit")
