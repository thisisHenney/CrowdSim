# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    # 이 PC의 PYTHONPATH에 D:\lib\가 들어있어서 pathex를 안 주면 PyInstaller가
    # 프로젝트 동봉 lib/nextlib 대신 D:\lib\nextlib(다른 프로젝트들과 공유하는 구버전)을
    # 잘못 집어서 번들에 넣는 문제가 있었다. lib/를 명시적으로 최우선 검색 경로로 지정해
    # PYTHONPATH 설정과 무관하게 항상 프로젝트 동봉 버전이 들어가도록 고정한다.
    pathex=['lib'],
    binaries=[],
    datas=[
        # 솔버 실행파일(RuntimeSPH2D.exe + CUDA/HASP DLL)은 Python import로 안 잡히므로 직접 포함
        ('solver', 'solver'),
        # 툴바/시작화면 아이콘, 로고 - 코드에서 app_info.path 기준 경로로 읽음
        ('view/main/icons', 'view/main/icons'),
        ('view/start/icons', 'view/start/icons'),
        ('logo.png', '.'),
        # nextlib(lib/nextlib)은 sys.path에 lib/를 추가해 최상위 nextlib 패키지로 import되므로,
        # 번들 안에서도 nextlib/... 경로에 있어야 코드의 __file__ 기준 아이콘 조회가 맞는다.
        ('lib/nextlib/widgets/icons', 'nextlib/widgets/icons'),
        ('lib/nextlib/vtk/res', 'nextlib/vtk/res'),
    ],
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
    [],
    exclude_binaries=True,
    name='main',
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
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
