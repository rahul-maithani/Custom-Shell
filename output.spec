# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['output.py'],
    pathex=['Logic'],
    binaries=[],
    datas=[('media\\\\*', 'media')],
    hiddenimports=['filemang_merge_pyqt5_logic', 'network_merge_pyqt5_logic', 'systeminfo_merged', 'battery_merged', 'disk_merged'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='output',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
