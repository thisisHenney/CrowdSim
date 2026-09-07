# -*- coding: utf-8 -*-
"""design-system 위젯을 CrowdSim 테마로 쓰기 위한 어댑터 (방식 A).

design-system/ADOPTION.md 의 "방식 A — 위젯만 가져오기"를 구현한다.
`view/theme.py` 는 그대로 두고, CrowdSim 에 없는 위젯(Field/Group/make_table/
Sparkline/Swatch)만 가져와 쓴다. 기존 화면의 모양은 바뀌지 않는다.

의도적으로 하지 않는 것 (ADOPTION.md 4.3 / 4.4):
  - design-system 의 apply_theme() 을 부르지 않는다.
    그 안의 setStyle("Fusion") 이 QSS 로 안 덮인 위젯을 전부 바꾸기 때문이다.
  - 폰트 크기를 건드리지 않는다. design-system 기본은 9pt 이고
    CrowdSim 은 main.py 에서 10pt 로 고정한다.

사용:
    from view.design_adapter import setup, widgets as W
    setup()                       # QApplication 생성 후 1회
    field = W.Field("밀도", "4.2", error="3.0 이상은 위험합니다")

테마를 바꾼 뒤(set_theme/toggle_theme)에는 refresh() 를 불러
위젯 색을 다시 맞춘다.
"""
import sys
from pathlib import Path

from view import theme

_DS = Path(__file__).resolve().parent.parent / 'design-system'

_ready = False
widgets = None      # setup() 이후 design-system 의 widgets 모듈


def _tokens():
    """CrowdSim 토큰(theme.py)을 design-system 이름으로 매핑한다.

    CrowdSim 에 없는 토큰(상태색 등)은 design-system tokens.py 에서
    현재 테마에 맞는 쪽을 가져온다 - 하드코딩하면 다크 테마에서 깨진다.
    """
    import tokens as _ds_tokens

    is_dark = theme._theme is theme.THEMES['dark']
    base = dict(_ds_tokens.DARK if is_dark else _ds_tokens.LIGHT)

    T = theme.T
    base.update({
        'surface':   T('BG'),
        'surface2':  T('BAR_BG'),
        'surface3':  T('ALT_ROW'),
        'ground':    T('BG'),
        'ink':       T('TEXT'),
        'ink2':      T('DIM'),
        # CrowdSim 은 보조 텍스트가 2단계뿐이라 ink3 도 DIM 을 쓴다.
        'ink3':      T('DIM'),
        'line':      T('BORDER'),
        'line_soft': T('BORDER'),
        'accent':    T('ACCENT'),
    })
    return base


def is_available():
    """design-system 소스가 옆에 있는지.

    이 폴더는 소스 트리에만 두는 참고 자료라 PyInstaller 배포본에는
    들어가지 않는다. 없으면 위젯을 쓸 수 없을 뿐 앱 동작에는 문제가 없다.
    """
    return (_DS / 'widgets.py').is_file()


def setup():
    """QApplication 생성 이후 1회 호출한다.

    design-system 소스가 없으면 아무것도 하지 않고 False를 반환한다.
    """
    global _ready, widgets

    if not is_available():
        return None

    if str(_DS) not in sys.path:
        sys.path.insert(0, str(_DS))

    import widgets as _w
    widgets = _w

    if not _ready:
        _w.init_fonts()
        _ready = True

    _w.set_theme(_tokens())
    return _w


def refresh():
    """테마 전환 후 design-system 위젯 색을 다시 맞춘다.

    이미 만들어진 위젯의 인라인 색까지 갱신되지는 않는다
    (design-system 위젯이 생성 시점에 색을 굽는다). 전환 후 새로
    만드는 위젯부터 적용된다.
    """
    if widgets is not None:
        widgets.set_theme(_tokens())
