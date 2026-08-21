"""uic가 생성한 `*_ui.py`에 없는, 원본 스키마상 누락된 입력 위젯을 코드로 덧붙이기 위한 헬퍼.

uic가 생성한 `*_ui.py`는 원본 대조를 위해 손대지 않는다.
대신 각 View의 `_initialize()`에서 부족한 입력란만 코드로 덧붙인다.

여기서 다루는 값들은 전부 "있으면 쓰고 없으면 키 자체를 만들지 않는다"가
원칙이다. 참조 json에 없던 키가 저장만으로 새로 생기면 왕복 정합성이
깨지기 때문이다.
"""
from PySide6.QtWidgets import (QCheckBox, QComboBox, QGroupBox, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QVBoxLayout,
                               QWidget)

LABEL_WIDTH = 96


def make_edit(width=None, placeholder=''):
    e = QLineEdit()
    if width:
        e.setFixedWidth(width)
    if placeholder:
        e.setPlaceholderText(placeholder)
    return e


def make_row(label, *widgets, label_width=LABEL_WIDTH, stretch_last=True):
    """`라벨 [위젯...]` 한 줄을 담은 QWidget을 만든다."""
    box = QWidget()
    lay = QHBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)

    lb = QLabel(label)
    lb.setMinimumWidth(label_width)
    lay.addWidget(lb)

    for w in widgets:
        lay.addWidget(w)
    if not stretch_last:
        lay.addStretch(1)
    return box


def make_group(title):
    g = QGroupBox(title)
    lay = QVBoxLayout(g)
    lay.setContentsMargins(8, 8, 8, 8)
    lay.setSpacing(4)
    return g, lay


def make_button_row(*buttons):
    box = QWidget()
    lay = QHBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)
    for b in buttons:
        lay.addWidget(b)
    return box


def parse_num(text, default=None):
    """'945' -> 945(int), '0.2' -> 0.2(float), '' -> default.

    정수로 적힌 값은 정수로 돌려준다. 참조 json이 `end_time: 945`처럼
    정수로 들고 있는 항목을 float으로 넓혀 쓰지 않기 위한 것이다.
    """
    s = (text or '').strip()
    if not s:
        return default
    try:
        if '.' in s or 'e' in s.lower():
            return float(s)
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return default


def parse_int_list(text):
    """'2, 3' -> [2, 3]. 비어 있으면 빈 리스트."""
    s = (text or '').strip()
    if not s:
        return []
    out = []
    for part in s.replace(';', ',').split(','):
        part = part.strip()
        if not part:
            continue
        v = parse_num(part)
        if v is not None:
            out.append(int(v))
    return out


def format_num(value):
    return '' if value is None else str(value)


def format_int_list(values):
    return ', '.join(str(v) for v in (values or []))


def parse_xy(x_text, y_text):
    """translate처럼 둘 다 채워졌을 때만 [x, y]를 만든다."""
    x = parse_num(x_text)
    y = parse_num(y_text)
    if x is None and y is None:
        return []
    return [x if x is not None else 0, y if y is not None else 0]
