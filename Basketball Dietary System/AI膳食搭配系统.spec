# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('mydb.db', '.'), ('食物数据库.xlsx', '.'), ('D:\\Download\\Anaconda\\envs\\Py_study\\DLLs\\pyexpat.pyd', '.'), ('D:\\Download\\Anaconda\\envs\\Py_study\\Library\\bin\\libexpat.dll', '.')]
binaries = []
hiddenimports = ['openpyxl', 'pandas', 'sqlite3', 'openai', 'PySide6', 'xml.parsers.expat', 'pyexpat']
tmp_ret = collect_all('openpyxl')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pandas')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main_guifan.py'],
    pathex=['D:\\Download\\Anaconda\\envs\\Py_study\\DLLs', 'D:\\Download\\Anaconda\\envs\\Py_study\\Library\\bin'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas.tests', 'pandas._testing', 'pandas.conftest', 'numpy.distutils', 'numpy.tests', 'PIL.ImageQt', 'PIL.ImageTk'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI膳食搭配系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI膳食搭配系统',
)
