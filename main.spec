# -*- mode: python ; coding: utf-8 -*-


def _solver_datas():
    """solver/ 에서 실행에 필요한 파일만 (원본, 번들경로) 쌍으로 만든다.

    RuntimeSPH2D.exe 는 같은 폴더의 DLL 들을 런타임에 찾으므로 exe/dll 은
    모두 넣어야 한다. service/haspdinst.exe 는 라이선스 동글 드라이버
    설치용이라 배포처에서 필요할 수 있어 함께 넣는다.
    문서(.pptx/.md)와 개발용 파일(.patch/.stl)만 제외한다.
    """
    import os

    SKIP_EXT = {'.pptx', '.md', '.patch', '.stl'}
    out = []
    for root, _dirs, files in os.walk('solver'):
        for fn in files:
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            src = os.path.join(root, fn)
            out.append((src, root))
    return out


a = Analysis(
    ['main.py'],
    # 이 PC의 PYTHONPATH에 D:\lib\가 들어있어서 pathex를 안 주면 PyInstaller가
    # 프로젝트 동봉 lib/nextlib 대신 D:\lib\nextlib(다른 프로젝트들과 공유하는 구버전)을
    # 잘못 집어서 번들에 넣는 문제가 있었다. lib/를 명시적으로 최우선 검색 경로로 지정해
    # PYTHONPATH 설정과 무관하게 항상 프로젝트 동봉 버전이 들어가도록 고정한다.
    pathex=['lib'],
    binaries=[],
    datas=[
        # 솔버 실행파일(RuntimeSPH2D.exe + CUDA/HASP DLL)은 Python import로 안 잡히므로 직접 포함.
        # solver/ 를 통째로 넣으면 실행에 필요 없는 문서/샘플까지 딸려 들어간다
        # (PPTX 10.9MB, README/전달문서 .md, sm75_gpu_arch.patch, crossing_bottleneck.stl).
        # 아래 _solver_datas()가 실행에 필요한 것만 골라 넣는다.
        *_solver_datas(),
        # 툴바/시작화면 아이콘, 로고 - 코드에서 app_info.path 기준 경로로 읽음
        ('view/main/icons', 'view/main/icons'),
        ('view/start/icons', 'view/start/icons'),
        ('logo.png', '.'),
        # nextlib(lib/nextlib)은 sys.path에 lib/를 추가해 최상위 nextlib 패키지로 import되므로,
        # 번들 안에서도 nextlib/... 경로에 있어야 코드의 __file__ 기준 아이콘 조회가 맞는다.
        ('lib/nextlib/widgets/icons', 'nextlib/widgets/icons'),
        ('lib/nextlib/vtk/res', 'nextlib/vtk/res'),
        # Scenario 독의 Common 프리셋 JSON - app_info.path 기준 경로로 읽음
        ('datarw/e8ight/presets', 'datarw/e8ight/presets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 이 프로젝트는 쓰지 않는데 venv 에 설치돼 있어 번들에 딸려 들어갈 수
        # 있는 것들 (합계 43MB). vtk/PySide6 를 import 해도 로드되지 않는 것을
        # 확인하고 제외했다.
        'matplotlib',
        'PIL',
        # 개발/테스트 전용
        'pytest',
        'IPython',
        'jupyter',
        'tkinter',
    ],
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
