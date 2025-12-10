# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['hexons_toolbox.py'],
    pathex=[],
    binaries=[],
    datas=[('tools\\\\MapleStory Quest Editor.exe', 'tools'), ('tools\\\\wz_icon_flattener_gui.exe', 'tools'), ('tools\\\\wz_icon_viewer_gui.exe', 'tools')],
    hiddenimports=[],
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
    name='Hexons Toolbox',
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
