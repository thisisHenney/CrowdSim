# -*- coding: utf-8 -*-
"""재사용 위젯 — QSS로 안 되는 것들의 최소 집합.

QSS가 커버하지 못하는 영역만 여기 둡니다:
  - CSS ::before/::after 의사요소 없음 -> 배지·스와치를 위젯으로
  - box-shadow 없음                   -> 필요하면 QGraphicsDropShadowEffect
  - 커스텀 그래픽                      -> QPainter
"""
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import (QPainter, QPainterPath, QPen, QBrush, QColor,
                           QFont, QIcon, QPixmap)
from PySide6.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QComboBox, QSizePolicy, QTableWidget,
                               QTableWidgetItem, QHeaderView, QAbstractItemView)

from tokens import LIGHT, FONT

T = LIGHT
_UI = "Segoe UI"
_MONO = "Consolas"


def init_fonts():
    """QApplication 생성 직후 1회 호출. 설치된 폰트로 스택을 해석합니다."""
    global _UI, _MONO
    from tokens import resolve_font
    _UI = resolve_font(FONT["ui_stack"])
    _MONO = resolve_font(FONT["mono_stack"])
    return _UI, _MONO


def set_theme(theme):
    global T
    T = theme


# ---------------------------------------------------------------- 텍스트
def label(text, size=None, color=None, bold=False, mono=False, upper=False):
    l = QLabel(text.upper() if upper else text)
    f = QFont(_MONO if mono else _UI, size or FONT["size"]["base"])
    f.setBold(bold)
    if upper:
        f.setLetterSpacing(QFont.AbsoluteSpacing, 0.8)
    l.setFont(f)
    if color:
        l.setStyleSheet("color:%s;background:transparent;" % color)
    return l


def hline():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("background:%s;max-height:1px;border:none;" % T["line_soft"])
    return f


# ---------------------------------------------------------------- 입력
class Field(QWidget):
    """라벨 + 입력 + 힌트/오류를 한 덩어리로 묶습니다.

    computed=True : 계산값. 읽기 전용 + 점선 테두리
    error="..."   : 오류. 빨간 테두리 + 메시지

    오류를 색만으로 표시하지 않는 것이 요점입니다.
    테두리 형태와 메시지를 함께 바꿔 색각 이상 사용자도 구분합니다.
    """

    def __init__(self, name, value, help_text=None, error=None,
                 computed=False, combo=False, parent=None):
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)
        v.addWidget(label(name, FONT["size"]["base"], T["ink2"]))

        if combo:
            w = QComboBox()
            w.addItem(value)
        else:
            w = QLineEdit(value)
            if computed:
                w.setReadOnly(True)
                w.setProperty("state", "computed")
            elif error:
                w.setProperty("state", "bad")
        w.setObjectName("field")
        w.setFont(QFont(_MONO, FONT["size"]["base"]))
        v.addWidget(w)
        self.input = w

        if error:
            v.addWidget(label("! " + error, FONT["size"]["sm"], T["crit"]))
        elif help_text:
            v.addWidget(label(help_text, FONT["size"]["sm"], T["ink3"]))


class Group(QFrame):
    """제목 바가 있는 카드. QGroupBox는 스타일링이 까다로워 직접 만듭니다."""

    def __init__(self, title, hint=None, title_color=None, parent=None):
        super().__init__(parent)
        self.setObjectName("group")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        head = QWidget()
        head.setObjectName("groupHead")
        hl = QHBoxLayout(head)
        hl.setContentsMargins(14, 8, 14, 8)
        hl.addWidget(label(title, FONT["size"]["base"], title_color or T["ink2"],
                           bold=True, mono=True, upper=True))
        hl.addStretch()
        if hint:
            hl.addWidget(label(hint, FONT["size"]["sm"], T["ink3"]))
        outer.addWidget(head)

        body = QWidget()
        body.setObjectName("groupBody")
        self.body = QVBoxLayout(body)
        self.body.setContentsMargins(14, 14, 14, 14)
        self.body.setSpacing(12)
        outer.addWidget(body)


def make_table(headers, rows, col_align=None):
    """읽기 전용 표. 숫자 열은 고정폭 + 우측 정렬로 자릿수를 맞춥니다."""
    t = QTableWidget(len(rows), len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setShowGrid(False)
    t.setSelectionMode(QAbstractItemView.NoSelection)
    t.setFocusPolicy(Qt.NoFocus)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.horizontalHeader().setFixedHeight(28)
    for r, row in enumerate(rows):
        t.setRowHeight(r, 26)
        for c, val in enumerate(row):
            it = QTableWidgetItem(str(val))
            align = (col_align or [])[c] if col_align and c < len(col_align) else "l"
            if align == "r":
                it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                it.setFont(QFont(_MONO, FONT["size"]["base"]))
            else:
                it.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                it.setForeground(QColor(T["ink2"]))
                it.setFont(QFont(_UI, FONT["size"]["base"]))
            t.setItem(r, c, it)
    t.setFixedHeight(28 + sum(t.rowHeight(r) for r in range(len(rows))) + 2)
    return t


# ---------------------------------------------------------------- 그래픽
class Sparkline(QWidget):
    """추세만 보여주는 소형 그래프. 축·눈금 없이 형태에 집중합니다."""

    def __init__(self, data, color, parent=None):
        super().__init__(parent)
        self.data, self.color = data, QColor(color)
        self.setMinimumHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, _):
        if len(self.data) < 2:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h, pad = self.width(), self.height(), 6
        mn, mx = min(self.data), max(self.data)
        rg = (mx - mn) or 1.0
        X = lambda i: (i / (len(self.data) - 1)) * (w - 2) + 1
        Y = lambda v: h - pad - ((v - mn) / rg) * (h - pad * 2)

        p.setPen(QPen(QColor(T["line_soft"]), 1))
        for k in range(3):
            y = pad + (h - pad * 2) * k / 2
            p.drawLine(QPointF(0, y), QPointF(w, y))

        path = QPainterPath(QPointF(X(0), h))
        for i, v in enumerate(self.data):
            path.lineTo(X(i), Y(v))
        path.lineTo(X(len(self.data) - 1), h)
        path.closeSubpath()
        fill = QColor(self.color)
        fill.setAlpha(33)
        p.fillPath(path, fill)

        line = QPainterPath(QPointF(X(0), Y(self.data[0])))
        for i, v in enumerate(self.data[1:], 1):
            line.lineTo(X(i), Y(v))
        p.strokePath(line, QPen(self.color, 1.6, Qt.SolidLine,
                                Qt.RoundCap, Qt.RoundJoin))

        lx, ly = X(len(self.data) - 1), Y(self.data[-1])
        p.setBrush(QBrush(self.color))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(lx, ly), 3, 3)


class Swatch(QWidget):
    """색 표식. CSS ::before 가 없어 위젯으로 만듭니다."""

    def __init__(self, color, size=9, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setFixedSize(size, size)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QBrush(self.color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 2, 2)


def make_icon(paint_fn, color, size=16):
    """QPainter 로 아이콘 생성. 고DPI 에서 안 깨집니다.

    paint_fn(painter, size) 형태의 함수를 받습니다.
    실제 프로젝트에서는 SVG 파일 + QIcon 을 권장합니다.
    """
    pm = QPixmap(size * 2, size * 2)
    pm.setDevicePixelRatio(2.0)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.scale(2, 2)
    pen = QPen(QColor(color), 1.6)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    paint_fn(p, size)
    p.end()
    return QIcon(pm)
