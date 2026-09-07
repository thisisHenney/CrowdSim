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


def set_fields_enabled(ui, names, enabled):
    """항목별 편집 위젯을 한꺼번에 활성/비활성한다.

    목록에 항목이 하나도 없을 때(= change_data(-1)) 입력란을 비우기만 하면
    빈 칸에 값을 쳐 넣을 수 있는 것처럼 보인다. 실제로는 저장할 대상이 없어
    입력이 사라지므로, "추가"를 누르기 전까지는 아예 비활성으로 둔다.

    ui 에 없는 이름은 조용히 건너뛴다. 패널마다 위젯 구성이 조금씩 다르고,
    일부는 _extra_ui 로 나중에 덧붙기 때문이다.
    """
    for name in names:
        w = getattr(ui, name, None)
        if w is not None:
            w.setEnabled(enabled)


def connect_autosave(ui, names, callback):
    """입력 위젯이 편집될 때마다 callback을 부르도록 연결한다.

    항목별 "저장" 버튼을 누르지 않아도 입력한 값이 메모리에 남게 하기
    위한 것이다. 파일에는 여전히 툴바 Save/Run 때만 기록된다.

    사용자가 직접 편집할 때만 발동하는 시그널을 고른다:
      - QLineEdit.textEdited (textChanged 가 아니다 - setText() 로 위젯을
        채울 때도 발동해서, 항목을 전환하면 새로 채운 값이 이전 항목에
        덮어써진다)
      - QComboBox.activated / QCheckBox.clicked / QRadioButton.clicked
        (currentIndexChanged/stateChanged 대신 사용자 조작 전용 시그널)
    """
    from PySide6.QtWidgets import (QCheckBox, QComboBox, QLineEdit,
                                   QRadioButton, QAbstractSpinBox)

    for name in names:
        w = getattr(ui, name, None)
        if w is None:
            continue
        if isinstance(w, QLineEdit):
            w.textEdited.connect(callback)
        elif isinstance(w, QComboBox):
            w.activated.connect(callback)
            if w.isEditable():
                w.lineEdit().textEdited.connect(callback)
        elif isinstance(w, (QCheckBox, QRadioButton)):
            w.clicked.connect(callback)
        elif isinstance(w, QAbstractSpinBox):
            w.editingFinished.connect(callback)
