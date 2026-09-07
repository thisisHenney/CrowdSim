# -*- coding: utf-8 -*-
"""디자인 토큰 — 색·간격·타이포의 단일 출처.

이 파일 하나만 바꾸면 전체 앱의 외양이 바뀝니다.
색을 위젯 코드에 직접 쓰지 마세요. 반드시 여기를 거칩니다.

대비율은 WCAG 2.1 기준으로 검증되었습니다 (verify_contrast() 참조).
"""

# ---------------------------------------------------------------- 색
LIGHT = dict(
    # 표면 — 낮은 숫자일수록 앞으로 나옴
    ground   = "#eef0f4",   # 앱 바깥 배경
    surface  = "#ffffff",   # 카드·입력 필드
    surface2 = "#f7f8fa",   # 레일·헤더 등 한 단 뒤
    surface3 = "#e8ebf0",   # 눌린 상태·칩

    # 잉크 — 낮은 숫자일수록 진함
    ink      = "#141821",   # 본문
    ink2     = "#4a5464",   # 라벨·보조
    ink3     = "#78828f",   # 힌트 (비필수 정보에만)

    # 선
    line      = "#d3d8e0",  # 구획선
    line_soft = "#e3e7ed",  # 표 내부 행 구분

    # 강조
    accent      = "#0b6bcb",
    accent_soft = "#e3eefc",
    accent_ink  = "#075099",  # accent_soft 위의 텍스트

    # 상태
    ok   = "#15803d", ok_soft = "#e3f4e9",
    warn = "#b45309",
    crit = "#b91c1c",

    # 도메인 — 물질 계열 (프로젝트마다 교체)
    explosive = "#c2410c", explosive_soft = "#fdecdf",
    solid     = "#6d5bd0", solid_soft     = "#eceafb",
    fluid     = "#0e7490", fluid_soft     = "#e0f2f7",

    # 터미널
    term_bg = "#12151c", term_ink = "#c8d2e0",
)

# 다크 테마는 역할을 뒤집되 이름은 그대로 둡니다.
# 위젯 코드는 T["surface"] 만 알면 되고 어떤 테마인지 몰라도 됩니다.
DARK = dict(
    ground   = "#0d1017",
    surface  = "#161a23",
    surface2 = "#1c212c",
    surface3 = "#28303d",

    ink      = "#e8ecf2",
    ink2     = "#a8b2c1",
    ink3     = "#6b7688",

    line      = "#2c3441",
    line_soft = "#222933",

    accent      = "#4d9bea",
    accent_soft = "#16283f",
    accent_ink  = "#8fc3f5",

    ok   = "#4ba86b", ok_soft = "#15291d",
    warn = "#d08a35",
    crit = "#e06666",

    explosive = "#e07a4a", explosive_soft = "#2e1d14",
    solid     = "#9b8ce0", solid_soft     = "#221e33",
    fluid     = "#4aa8c0", fluid_soft     = "#132630",

    term_bg = "#0a0d12", term_ink = "#c8d2e0",
)

# ---------------------------------------------------------------- 간격
# 4px 격자. 임의의 숫자를 쓰지 말고 여기서 고릅니다.
SP = {"xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16, "2xl": 20, "3xl": 24}

RADIUS = {"sm": 3, "md": 5, "lg": 6, "pill": 99}

# ---------------------------------------------------------------- 타이포
# 두 종류만 씁니다: UI용 산세리프, 숫자·코드용 고정폭.
FONT = dict(
    ui_stack   = ["IBM Plex Sans", "Segoe UI", "Noto Sans KR", "sans-serif"],
    mono_stack = ["IBM Plex Mono", "Cascadia Mono", "Consolas", "monospace"],
    size = {"xs": 7, "sm": 8, "base": 9, "md": 10, "lg": 11, "xl": 12.5},
)


def resolve_font(candidates):
    """설치된 첫 폰트를 반환. QApplication 생성 후 호출해야 합니다."""
    from PySide6.QtGui import QFontDatabase
    installed = set(QFontDatabase.families())
    for name in candidates:
        if name in installed:
            return name
    return candidates[-1]


def verify_contrast(theme=None, min_ratio=4.5):
    """WCAG 대비율 검사. CI에서 회귀 방지용으로 부를 수 있습니다.

    반환: [(용도, 전경, 배경, 대비율, 통과여부), ...]
    """
    T = theme or LIGHT

    def _lum(h):
        h = h.lstrip("#")
        c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b = map(f, c)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _ratio(a, b):
        l1, l2 = sorted([_lum(a), _lum(b)], reverse=True)
        return (l1 + 0.05) / (l2 + 0.05)

    # ink3(힌트)는 비필수 정보이므로 3.0 기준을 적용합니다.
    checks = [
        ("본문",        "ink",        "surface",     min_ratio),
        ("보조 텍스트", "ink2",       "surface",     min_ratio),
        ("힌트",        "ink3",       "surface",     3.0),
        ("강조",        "accent",     "surface",     min_ratio),
        ("선택 상태",   "accent_ink", "accent_soft", min_ratio),
        ("정상",        "ok",         "surface",     min_ratio),
        ("경고",        "warn",       "surface",     min_ratio),
        ("오류",        "crit",       "surface",     min_ratio),
        ("터미널",      "term_ink",   "term_bg",     min_ratio),
    ]
    out = []
    for name, fg, bg, need in checks:
        r = _ratio(T[fg], T[bg])
        out.append((name, T[fg], T[bg], round(r, 2), r >= need))
    return out


if __name__ == "__main__":
    for theme_name, theme in (("LIGHT", LIGHT), ("DARK", DARK)):
        print(f"\n=== {theme_name} ===")
        for name, fg, bg, ratio, ok in verify_contrast(theme):
            print(f"  {name:<12} {fg} on {bg}  {ratio:>6.2f}  {'OK' if ok else 'FAIL'}")
