# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ["desktop_backend_entry.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "app.desktop_main",
        "app.api.v1.endpoints.desktop",
        "app.api.v1.endpoints.literature",
        "app.services.literature_service",
        "services.ai_providers",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="llb-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="llb-backend",
)
