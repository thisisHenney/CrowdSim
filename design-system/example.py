# -*- coding: utf-8 -*-
"""디자인 시스템 최소 사용 예 — 새 프로젝트는 이 파일을 복사해 시작합니다.

실행:
    python example.py            # 라이트
    python example.py --dark     # 다크
    python example.py --shot     # 두 테마 스크린샷 저장 후 종료
"""
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QTabWidget,
                               QScrollArea, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from tokens import LIGHT, DARK, FONT
from stylesheet import apply_theme
import widgets as W


class Demo(QMainWindow):
    def __init__(self, theme):
        super().__init__()
        self.setWindowTitle("Design System — 사용 예")
        self.resize(1080, 620)

        central = QWidget()
        central.setObjectName("root")
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._rail(theme))
        root.addWidget(self._work(theme), 1)
        root.addWidget(self._insp(theme))
        self.setCentralWidget(central)

    # ---- 좌: 작업 단계
    def _rail(self, T):
        rail = QWidget()
        rail.setObjectName("rail")
        rail.setFixedWidth(190)
        v = QVBoxLayout(rail)
        v.setContentsMargins(8, 10, 8, 8)
        v.setSpacing(2)

        for head, items in (("입력", ["형상", "물성", "경계조건"]),
                            ("계산", ["설정", "실행"]),
                            ("결과", ["가시화"])):
            lb = W.label(head, FONT["size"]["sm"], T["ink3"], bold=True,
                         mono=True, upper=True)
            lb.setContentsMargins(10, 12, 10, 4)
            v.addWidget(lb)
            for i, name in enumerate(items):
                b = QPushButton("  " + name)
                b.setObjectName("nav")
                b.setCheckable(True)
                b.setChecked(head == "입력" and i == 0)
                b.setCursor(Qt.PointingHandCursor)
                v.addWidget(b)

        v.addStretch()
        v.addWidget(W.hline())
        foot = W.label("design-system v1", FONT["size"]["xs"], T["ink3"], mono=True)
        foot.setContentsMargins(10, 8, 10, 4)
        v.addWidget(foot)
        return rail

    # ---- 중: 작업 영역
    def _work(self, T):
        tabs = QTabWidget()
        tabs.setObjectName("work")
        tabs.setDocumentMode(True)

        page = QWidget()
        page.setObjectName("pane")
        v = QVBoxLayout(page)
        v.setContentsMargins(20, 20, 20, 20)
        v.setSpacing(16)

        # 입력 필드 3가지 상태
        g = W.Group("입력 필드", "정상 / 계산값 / 오류")
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(12)
        grid.addWidget(W.Field("이름", "case_01",
                               help_text="공백은 _ 로 치환됩니다"), 0, 0)
        grid.addWidget(W.Field("셀 개수", "98,280",
                               help_text="자동 계산됨", computed=True), 0, 1)
        grid.addWidget(W.Field("종횡비", "84.5",
                               error="20 이하를 권장합니다"), 0, 2)
        g.body.addLayout(grid)
        v.addWidget(g)

        # 표
        g2 = W.Group("데이터 표", "숫자는 우측 정렬")
        g2.body.addWidget(W.make_table(
            ["축", "최소", "최대", "셀"],
            [["X", "0.0", "0.20", "78"],
             ["Y", "0.0", "9.10", "42"],
             ["Z", "0.0", "0.20", "30"]],
            col_align=["l", "r", "r", "r"]))
        row = QHBoxLayout()
        row.setSpacing(8)
        b1 = QPushButton("실행")
        b1.setObjectName("btnPri")
        b1.setCursor(Qt.PointingHandCursor)
        b2 = QPushButton("초기화")
        b2.setObjectName("btn")
        b2.setCursor(Qt.PointingHandCursor)
        row.addWidget(b1)
        row.addWidget(b2)
        row.addStretch()
        g2.body.addLayout(row)
        v.addWidget(g2)

        # 스파크라인
        g3 = W.Group("추세")
        import math
        data = [0.9 * math.exp(-i * 0.04) + 0.2 + math.sin(i * 0.5) * 0.02
                for i in range(60)]
        g3.body.addWidget(W.Sparkline(data, T["accent"]))
        v.addWidget(g3)

        v.addStretch()
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        sa.setWidget(page)
        tabs.addTab(sa, "설정")
        return tabs

    # ---- 우: 정보 패널
    def _insp(self, T):
        insp = QWidget()
        insp.setObjectName("insp")
        insp.setFixedWidth(230)
        v = QVBoxLayout(insp)
        v.setContentsMargins(14, 14, 14, 14)
        v.setSpacing(14)

        v.addWidget(W.label("상태", FONT["size"]["sm"], T["ink3"],
                            bold=True, mono=True, upper=True))
        for icon, col, text in (("v", T["ok"], "형상 로드됨"),
                                ("!", T["warn"], "종횡비 확인 필요"),
                                ("-", T["ink3"], "물성 미설정")):
            r = QHBoxLayout()
            r.setSpacing(8)
            ic = W.label(icon, FONT["size"]["md"], col, bold=True, mono=True)
            ic.setFixedWidth(12)
            r.addWidget(ic, 0, Qt.AlignTop)
            tx = W.label(text, FONT["size"]["base"], T["ink2"])
            tx.setWordWrap(True)
            r.addWidget(tx, 1)
            v.addLayout(r)

        v.addWidget(W.hline())
        v.addWidget(W.label("물질", FONT["size"]["sm"], T["ink3"],
                            bold=True, mono=True, upper=True))
        for name, key in (("화약", "explosive"), ("고체", "solid"), ("유체", "fluid")):
            r = QHBoxLayout()
            r.setSpacing(8)
            r.addWidget(W.Swatch(T[key]), 0, Qt.AlignVCenter)
            r.addWidget(W.label(name, FONT["size"]["base"], T["ink2"]), 1)
            v.addLayout(r)

        v.addStretch()
        return insp


def main():
    app = QApplication(sys.argv)
    dark = "--dark" in sys.argv
    theme = DARK if dark else LIGHT

    W.init_fonts()          # 폰트 해석은 QApplication 이후에
    W.set_theme(theme)
    apply_theme(app, theme)
    app.setFont(QFont(W._UI, FONT["size"]["base"]))

    w = Demo(theme)
    w.show()

    if "--shot" in sys.argv:
        from pathlib import Path
        from PySide6.QtCore import QTimer
        out = Path(__file__).parent / "shots"
        out.mkdir(exist_ok=True)

        def grab_light():
            w.grab().save(str(out / "light.png"))
            # 다크로 전환 — 토큰만 바꾸면 되는지 확인
            W.set_theme(DARK)
            apply_theme(app, DARK)
            w2 = Demo(DARK)
            w2.resize(1080, 620)
            w2.show()
            QTimer.singleShot(500, lambda: (w2.grab().save(str(out / "dark.png")),
                                            app.quit()))
        QTimer.singleShot(700, grab_light)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
