# -*- coding: utf-8 -*-
"""방식 A 검증 — CrowdSim theme.py 토큰으로 design-system 위젯을 쓴다.

ADOPTION.md 3장 "방식 A"의 코드가 실제로 동작하는지 확인합니다.
기존 theme.py 를 그대로 두고 위젯만 가져오는 방식입니다.

실행:
    .venv\\Scripts\\python.exe design-system\\adapter_example.py
"""
import sys
from pathlib import Path

# CrowdSim 프로젝트 루트를 경로에 추가
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "lib"))     # nextlib
sys.path.insert(0, str(_ROOT))             # view.theme
sys.path.insert(0, str(Path(__file__).parent))  # design-system

from PySide6.QtWidgets import QApplication

# Windows 콘솔(CP949)에서 출력이 죽지 않도록
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def build_adapter():
    """CrowdSim 토큰을 design-system 이름으로 매핑합니다.

    CrowdSim 에 없는 토큰(상태색 등)은 값을 직접 넣습니다.
    """
    from view.theme import T as _T
    return {
        # CrowdSim 에 있는 것 — theme.py 를 그대로 따라갑니다
        "surface":   _T("BG"),
        "surface2":  _T("BAR_BG"),
        "surface3":  _T("ALT_ROW"),
        "ground":    _T("BG"),
        "ink":       _T("TEXT"),
        "ink2":      _T("DIM"),
        "ink3":      _T("DIM"),      # CrowdSim 은 2단계뿐이라 DIM 을 공유
        "line":      _T("BORDER"),
        "line_soft": _T("BORDER"),
        "accent":    _T("ACCENT"),

        # CrowdSim 에 없는 것 — 직접 지정
        "accent_soft": "#e3eefc", "accent_ink": "#075099",
        "ok":   "#15803d", "ok_soft": "#e3f4e9",
        "warn": "#b45309",
        "crit": "#b91c1c",
        "explosive": "#c2410c", "explosive_soft": "#fdecdf",
        "solid":     "#6d5bd0", "solid_soft":     "#eceafb",
        "fluid":     "#0e7490", "fluid_soft":     "#e0f2f7",
        "term_bg":   "#12151c", "term_ink":       "#c8d2e0",
    }


def main():
    app = QApplication(sys.argv)

    adapter = build_adapter()
    print("CrowdSim 토큰 매핑:")
    for k in ("surface", "ink", "ink2", "accent", "line"):
        print(f"   {k:<10} {adapter[k]}")

    import widgets as W
    W.init_fonts()          # QApplication 이후에 호출해야 합니다
    W.set_theme(adapter)

    # 기존 CrowdSim QSS 를 그대로 씁니다 — apply_theme() 을 쓰지 않습니다
    from view.theme import build_css
    app.setStyleSheet(build_css())

    made = [
        W.Field("체류 인원", "1240", help_text="명"),
        W.Field("밀도", "4.2", error="3.0 이상은 위험 수준입니다"),
        W.Group("영역 설정", "zone"),
        W.make_table(["구역", "면적", "밀도"],
                     [["A", "120", "1.4"], ["B", "80", "2.1"]],
                     col_align=["l", "r", "r"]),
        W.Sparkline([1, 3, 2, 5, 4, 6, 5], adapter["accent"]),
        W.Swatch(adapter["accent"]),
    ]
    print("\n위젯 생성:", [type(x).__name__ for x in made])
    print("기존 build_css():", len(build_css()), "chars, 공존 확인")
    print("\nPASSED — 방식 A 가 동작합니다")

    if "--show" in sys.argv or "--shot" in sys.argv:
        from PySide6.QtWidgets import QWidget, QVBoxLayout
        w = QWidget()
        w.setWindowTitle("방식 A: CrowdSim 토큰 + design-system 위젯")
        v = QVBoxLayout(w)
        for x in made[:5]:
            v.addWidget(x)
        w.resize(460, 520)
        w.show()

        if "--shot" in sys.argv:
            from PySide6.QtCore import QTimer
            out = Path(__file__).parent / "shots" / "adapter.png"
            out.parent.mkdir(exist_ok=True)
            QTimer.singleShot(700, lambda: (w.grab().save(str(out)), app.quit()))

        sys.exit(app.exec())


if __name__ == "__main__":
    main()
