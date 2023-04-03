# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
sys.setrecursionlimit(25000)
a = Analysis(['ppXAFS_auto_dev_pypt.py'],
             pathex=['/Users/uemura_y/Library/Mobile Documents/com~apple~CloudDocs/from_OneDrive/python3/py_ppXAFS_dev_auto'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ppXAFS_auto_dev_pypt',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='ppXAFS_auto_dev_pypt.app',
             icon=None,
             bundle_identifier=None)
