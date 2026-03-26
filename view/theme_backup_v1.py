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
        "BG":      "#eaeaf2",
        "CARD":    "#ffffff",
        "BORDER":  "#c4c4d4",
        "TEXT":    "#111128",
        "DIM":     "#4a4a68",
        "ACCENT":  "#2563eb",
        "BAR_BG":  "#d4d4e0",
        "ALT_ROW": "#f4f4f8",
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
    background: {T('CARD')};
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
    background: {T('CARD')};
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
    background: {T('CARD')};
    border-bottom: 1px solid {T('BORDER')};
    spacing: 2px;
    padding: 3px 4px;
}}
QToolButton {{
    background: transparent;
    border: none;
    border-radius: 5px;
    padding: 4px;
    color: {T('TEXT')};
}}
QToolButton:hover {{
    background: {T('BORDER')};
}}
QToolButton:pressed {{
    background: {T('ACCENT')};
}}
QToolBar::separator {{
    width: 1px;
    background: {T('BORDER')};
    margin: 4px 2px;
}}

/* StatusBar */
QStatusBar {{
    background: {T('CARD')};
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
    border-radius: 5px;
    padding: 4px 6px;
    color: {T('TEXT')};
}}
QPushButton:hover {{
    background: {T('BORDER')};
    border-color: {T('ACCENT')};
}}
QPushButton:pressed {{
    background: {T('ACCENT')};
    color: #ffffff;
    border-color: {T('ACCENT')};
}}
QPushButton:disabled {{
    color: {T('DIM')};
    border-color: {T('BORDER')};
    background: {T('BG')};
}}

/* Input fields */
QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QPlainTextEdit {{
    background: {T('CARD')};
    border: 1px solid {T('BORDER')};
    border-radius: 4px;
    padding: 3px 6px;
    color: {T('TEXT')};
    selection-background-color: {T('ACCENT')};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {T('ACCENT')};
}}
QLineEdit:read-only {{
    color: {T('DIM')};
    background: {T('BG')};
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
    background: {T('ACCENT')};
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
    border-radius: 4px;
    padding: 3px 6px;
    color: {T('TEXT')};
}}
QComboBox:focus {{
    border-color: {T('ACCENT')};
}}
QComboBox::drop-down {{
    border-left: 1px solid {T('BORDER')};
    background: {T('BAR_BG')};
    width: 22px;
    border-radius: 0 4px 4px 0;
}}
QComboBox::down-arrow {{
    image: url({_ICONS}/arrow_down.svg);
    width: 10px;
    height: 6px;
}}
QComboBox QAbstractItemView {{
    background: {T('CARD')};
    border: 1px solid {T('BORDER')};
    selection-background-color: {T('ACCENT')};
    selection-color: #ffffff;
    border-radius: 4px;
    padding: 2px;
}}

/* TreeWidget */
QTreeWidget, QTreeView, QListWidget, QListView {{
    background: {T('CARD')};
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    alternate-background-color: {T('ALT_ROW')};
    outline: none;
}}
QTreeWidget::item, QTreeView::item,
QListWidget::item, QListView::item {{
    padding: 3px 2px;
    border-radius: 3px;
}}
QTreeWidget::item:selected, QTreeView::item:selected,
QListWidget::item:selected, QListView::item:selected {{
    background: {T('ACCENT')};
    color: #ffffff;
}}
QTreeWidget::item:hover, QTreeView::item:hover,
QListWidget::item:hover, QListView::item:hover {{
    background: {T('BORDER')};
}}
QHeaderView::section {{
    background: {T('BAR_BG')};
    color: {T('DIM')};
    border: none;
    border-right: 1px solid {T('BORDER')};
    border-bottom: 1px solid {T('BORDER')};
    padding: 4px 8px;
    font-size: 9pt;
}}

/* ScrollBar */
QScrollBar:vertical {{
    background: {T('BG')};
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {T('BORDER')};
    border-radius: 4px;
    min-height: 24px;
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
    background: {T('BG')};
    height: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {T('BORDER')};
    border-radius: 4px;
    min-width: 24px;
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
    margin-top: 14px;
    padding-top: 8px;
}}
QGroupBox::title {{
    color: {T('TEXT')};
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    font-size: 9pt;
    font-weight: bold;
}}

/* Splitter */
QSplitter::handle {{
    background: {T('BORDER')};
}}
QSplitter::handle:horizontal {{
    width: 2px;
}}
QSplitter::handle:vertical {{
    height: 2px;
}}

/* TabWidget */
QTabWidget::pane {{
    border: 1px solid {T('BORDER')};
    border-radius: 6px;
    background: {T('CARD')};
    top: -1px;
}}
QTabBar::tab {{
    background: {T('BG')};
    border: 1px solid {T('BORDER')};
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    padding: 5px 14px;
    color: {T('DIM')};
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background: {T('CARD')};
    color: {T('TEXT')};
    border-bottom: 2px solid {T('ACCENT')};
}}
QTabBar::tab:hover {{
    color: {T('TEXT')};
    background: {T('BORDER')};
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
    border: 2px solid {T('ACCENT')};
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
    border: 2px solid {T('ACCENT')};
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
    border: 2px solid {T('ACCENT')};
    border-radius: 7px;
}}

/* Dock widget */
QDockWidget {{
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}
QDockWidget::title {{
    background: {T('CARD')};
    color: {T('DIM')};
    border-bottom: 1px solid {T('BORDER')};
    padding: 4px 8px;
    font-size: 9pt;
}}

/* ProgressBar */
QProgressBar {{
    background: {T('BAR_BG')};
    border: 1px solid {T('BORDER')};
    border-radius: 4px;
    color: {T('TEXT')};
    text-align: center;
    font-size: 9pt;
}}
QProgressBar::chunk {{
    background: {T('ACCENT')};
    border-radius: 3px;
}}

/* Tooltips */
QToolTip {{
    background: {T('CARD')};
    color: {T('TEXT')};
    border: 1px solid {T('BORDER')};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 9pt;
}}
"""
