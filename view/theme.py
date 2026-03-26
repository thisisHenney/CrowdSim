import os
import nextlib as _nextlib
_ICONS = os.path.join(os.path.dirname(_nextlib.__file__), "widgets/icons").replace("\\", "/")

THEMES = {
    "dark": {
        "BG":      "#1e1e2e",
        "CARD":    "#2a2a3d",
        "BORDER":  "#3e3e5a",
        "TEXT":    "#e8e8f8",
        "DIM":     "#9898b8",
        "ACCENT":  "#4a9eff",
        "BAR_BG":  "#14141f",
        "ALT_ROW": "#252535",
    },
    "light": {
        "BG":      "#ffffff",   # 흰색 배경
        "CARD":    "#ffffff",   # 입력필드 흰색
        "BORDER":  "#d0d7de",   # 명확한 회색 경계선
        "TEXT":    "#1f2328",   # 진한 텍스트
        "DIM":     "#636c76",   # 흐린 보조 텍스트
        "ACCENT":  "#2563eb",   # 파란 강조색
        "BAR_BG":  "#f6f8fa",   # 연한 회색 (툴바·버튼 배경)
        "ALT_ROW": "#f6f8fa",   # 교차 행 색
    },
}

_theme = THEMES["light"]


def T(key):
    return _theme[key]


def set_theme(name: str):
    global _theme
    _theme = THEMES[name]


def toggle_theme():
    global _theme
    _theme = THEMES["light"] if _theme is THEMES["dark"] else THEMES["dark"]


def build_css() -> str:
    _radio_checked = f"{_ICONS}/radio_checked_{'dark' if _theme is THEMES['dark'] else 'light'}.svg"
    return f"""
/* Base */
QWidget {{
    background-color: {T('BG')};
    color: {T('TEXT')};
    font-family: "Segoe UI";
    font-size: 10pt;
}}

/* Main windows */
QMainWindow, QDialog {{
    background: {T('BG')};
}}

/* MenuBar */
QMenuBar {{
    background: {T('BAR_BG')};
    color: {T('TEXT')};
    border-bottom: 1px solid {T('BORDER')};
    padding: 2px;
}}
QMenuBar::item {{
    padding: 4px 10px;
    border-radius: 4px;
    background: transparent;
}}
QMenuBar::item:selected {{
    background: {T('BORDER')};
}}
QMenu {{
    background: {T('BG')};
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 5px 20px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background: {T('ACCENT')};
    color: #ffffff;
}}
QMenu::separator {{
    height: 1px;
    background: {T('BORDER')};
    margin: 4px 8px;
}}

/* ToolBar */
QToolBar {{
    background: {T('BAR_BG')};
    border-bottom: 1px solid {T('BORDER')};
    spacing: 2px;
    padding: 3px 6px;
}}
QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 4px;
    color: {T('TEXT')};
}}
QToolButton:hover {{
    background: {T('BG')};
    border-color: {T('BORDER')};
}}
QToolButton:pressed {{
    background: #dbeafe;
    border-color: {T('ACCENT')};
}}
QToolBar::separator {{
    width: 1px;
    background: {T('BORDER')};
    margin: 4px 3px;
}}

/* StatusBar */
QStatusBar {{
    background: {T('BAR_BG')};
    color: {T('DIM')};
    border-top: 1px solid {T('BORDER')};
    font-size: 9pt;
}}

/* Labels */
QLabel {{
    background: transparent;
    color: {T('TEXT')};
}}

/* Buttons */
QPushButton {{
    background: {T('BAR_BG')};
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    padding: 5px 12px;
    color: {T('TEXT')};
    font-weight: 500;
}}
QPushButton:hover {{
    background: #eff6ff;
    border-color: {T('ACCENT')};
    color: {T('ACCENT')};
}}
QPushButton:pressed {{
    background: #dbeafe;
    border-color: {T('ACCENT')};
    color: {T('ACCENT')};
}}
QPushButton:disabled {{
    color: {T('DIM')};
    border-color: {T('BORDER')};
    background: {T('BAR_BG')};
}}

/* Input fields */
QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QPlainTextEdit {{
    background: {T('CARD')};
    border: 1px solid {T('BORDER')};
    border-radius: 5px;
    padding: 4px 7px;
    color: {T('TEXT')};
    selection-background-color: {T('ACCENT')};
}}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover,
QTextEdit:hover, QPlainTextEdit:hover {{
    border-color: {T('ACCENT')};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {T('ACCENT')};
    padding: 3px 6px;
}}
QLineEdit:read-only {{
    color: {T('DIM')};
    background: {T('BAR_BG')};
}}
QTextEdit:read-only, QPlainTextEdit:read-only {{
    background: {T('CARD')};
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background: {T('BAR_BG')};
    border: none;
    border-radius: 2px;
    width: 16px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background: #dbeafe;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url({_ICONS}/arrow_up.svg);
    width: 8px;
    height: 5px;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url({_ICONS}/arrow_down.svg);
    width: 8px;
    height: 5px;
}}

/* ComboBox */
QComboBox {{
    background: {T('CARD')};
    border: 1px solid {T('BORDER')};
    border-radius: 5px;
    padding: 4px 7px;
    color: {T('TEXT')};
}}
QComboBox:focus {{
    border: 2px solid {T('ACCENT')};
    padding: 3px 6px;
}}
QComboBox::drop-down {{
    border-left: 1px solid {T('BORDER')};
    background: {T('BAR_BG')};
    width: 22px;
    border-radius: 0 5px 5px 0;
}}
QComboBox::down-arrow {{
    image: url({_ICONS}/arrow_down.svg);
    width: 10px;
    height: 6px;
}}
QComboBox QAbstractItemView {{
    background: {T('BG')};
    border: 1px solid {T('BORDER')};
    selection-background-color: {T('ACCENT')};
    selection-color: #ffffff;
    border-radius: 5px;
    padding: 2px;
    outline: none;
}}

/* ScrollArea */
QScrollArea {{
    background: {T('BAR_BG')};
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: {T('BAR_BG')};
}}

/* TreeWidget / ListView */
QTreeWidget, QTreeView, QListWidget, QListView {{
    background: {T('BG')};
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    alternate-background-color: {T('ALT_ROW')};
    outline: none;
}}
QTreeWidget::item, QTreeView::item,
QListWidget::item, QListView::item {{
    padding: 3px 4px;
    border-radius: 4px;
}}
QTreeWidget::item:selected, QTreeView::item:selected,
QListWidget::item:selected, QListView::item:selected {{
    background: {T('ACCENT')};
    color: #ffffff;
}}
QTreeWidget::item:hover, QTreeView::item:hover,
QListWidget::item:hover, QListView::item:hover {{
    background: #eff6ff;
    color: {T('TEXT')};
}}
QHeaderView::section {{
    background: {T('BAR_BG')};
    color: {T('DIM')};
    border: none;
    border-right: 1px solid {T('BORDER')};
    border-bottom: 1px solid {T('BORDER')};
    padding: 4px 8px;
    font-size: 9pt;
    font-weight: 600;
}}

/* ScrollBar */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border-radius: 4px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {T('BORDER')};
    border-radius: 4px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{
    background: {T('DIM')};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    height: 0;
    background: none;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border-radius: 4px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {T('BORDER')};
    border-radius: 4px;
    min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {T('DIM')};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    width: 0;
    background: none;
}}

/* GroupBox */
QGroupBox {{
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    margin-top: 16px;
    padding-top: 8px;
    background: {T('BG')};
}}
QGroupBox::title {{
    color: {T('DIM')};
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    font-size: 9pt;
    font-weight: 600;
    background: {T('BG')};
}}

/* Disabled state (e.g. unchecked QGroupBox children) */
QLabel:disabled {{
    color: {T('BORDER')};
}}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
QTextEdit:disabled, QPlainTextEdit:disabled {{
    background: {T('BAR_BG')};
    color: {T('BORDER')};
    border-color: {T('BORDER')};
}}
QComboBox:disabled {{
    background: {T('BAR_BG')};
    color: {T('BORDER')};
    border-color: {T('BORDER')};
}}
QCheckBox:disabled, QRadioButton:disabled {{
    color: {T('BORDER')};
}}
QCheckBox::indicator:disabled, QRadioButton::indicator:disabled {{
    background: {T('BAR_BG')};
    border-color: {T('BORDER')};
}}
QCheckBox::indicator:checked:disabled {{
    background: {T('BAR_BG')};
    border-color: {T('BORDER')};
    image: none;
}}
QRadioButton::indicator:checked:disabled {{
    background: {T('BAR_BG')};
    border-color: {T('BORDER')};
    image: none;
}}

/* Splitter */
QSplitter::handle {{
    background: {T('BORDER')};
}}
QSplitter::handle:horizontal {{
    width: 1px;
}}
QSplitter::handle:vertical {{
    height: 1px;
}}

/* TabWidget */
QTabWidget::pane {{
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    background: {T('BG')};
    top: -1px;
}}
QTabBar::tab {{
    background: {T('BAR_BG')};
    border: 1px solid {T('BORDER')};
    border-bottom: none;
    border-radius: 5px 5px 0 0;
    padding: 5px 16px;
    color: {T('DIM')};
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background: {T('BG')};
    color: {T('ACCENT')};
    border-bottom: 2px solid {T('ACCENT')};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {T('TEXT')};
    background: #eff6ff;
    border-color: {T('ACCENT')};
}}

/* CheckBox / RadioButton */
QCheckBox, QRadioButton {{
    color: {T('TEXT')};
    spacing: 6px;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {T('ACCENT')};
    border-radius: 3px;
    background: {T('CARD')};
}}
QRadioButton::indicator {{
    border-radius: 7px;
}}
QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
    background: #dbeafe;
    border: 1.5px solid {T('ACCENT')};
}}
QRadioButton::indicator:hover {{
    border-radius: 7px;
}}
QCheckBox::indicator:checked {{
    background: {T('CARD')};
    border-color: {T('ACCENT')};
    image: url({_ICONS}/checkmark_blue.svg);
}}
QCheckBox::indicator:checked:hover {{
    background: #dbeafe;
    border: 1.5px solid {T('ACCENT')};
    image: url({_ICONS}/checkmark_blue.svg);
}}
QRadioButton::indicator:checked {{
    image: url({_radio_checked});
    background: transparent;
    border: none;
}}
QRadioButton::indicator:checked:hover {{
    image: url({_radio_checked});
    background: #dbeafe;
    border: 1.5px solid {T('ACCENT')};
    border-radius: 7px;
}}

/* Dock widget */
QDockWidget {{
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}
QDockWidget::title {{
    background: {T('BAR_BG')};
    color: {T('DIM')};
    border-bottom: 1px solid {T('BORDER')};
    padding: 5px 8px;
    font-size: 9pt;
    font-weight: 600;
}}

/* ProgressBar */
QProgressBar {{
    background: {T('BAR_BG')};
    border: 1px solid {T('BORDER')};
    border-radius: 5px;
    color: {T('TEXT')};
    text-align: center;
    font-size: 9pt;
}}
QProgressBar::chunk {{
    background: {T('ACCENT')};
    border-radius: 4px;
}}

/* Tooltips */
QToolTip {{
    background: {T('BG')};
    color: {T('TEXT')};
    border: 1px solid {T('BORDER')};
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 9pt;
}}
"""
