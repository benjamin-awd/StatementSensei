# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules("webapp")
hiddenimports += collect_submodules("pybadges")

a = Analysis(
    ["entrypoint.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=["./hooks"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "altair", "matplotlib", "bokeh", "graphviz", "tensorflow"],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    a.scripts,
    [],
    exclude_binaries=False,
    name="entrypoint",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
