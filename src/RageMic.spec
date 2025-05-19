# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['rage.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=['ttkbootstrap.constants', 'pyaudio'],
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
    name='RageMic',
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
    icon=['icon.png'],
)
app = BUNDLE(
    exe,
    name='RageMic.app',
    icon='icon.png',
    bundle_identifier=None,
)
