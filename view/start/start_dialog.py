from pathlib import Path
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QPoint, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QLinearGradient

from nextlib.utils.ui import load_ui
from nextlib.utils.file import make_dir, is_dir
from nextlib.utils.picture import Picture
from nextlib.widgets.recent_list.recent_list import RecentList
from nextlib.dialogbox.dialogbox import DirDialogBox
from nextlib.widgets.messagebox import messagebox_warning
from nextlib.widgets.icon import add_icon

from view.main.main_window_view import MainWindowView
from view.start.start_dialog_ui import Ui_StartDialog


class StartDialog(QDialog):
    def __init__(self, app_info):
        super().__init__()
        self.app_info = app_info

        self._ui = load_ui(self, Ui_StartDialog)
        self.recent_list = None

        self.main_view = MainWindowView(app_info)

        self._initialize()

    def _initialize(self):
        self.setWindowTitle('Project Manager')

        # 프레임 없는 둥근 모서리 윈도우
        self._shadow_margin = 4
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 그림자 여백 확보
        orig_size = self.size()
        self.setFixedSize(orig_size.width() + self._shadow_margin * 2,
                          orig_size.height() + self._shadow_margin * 2)
        self.setContentsMargins(self._shadow_margin, self._shadow_margin,
                                self._shadow_margin, self._shadow_margin)

        self._init_program()
        self._init_connect_menu()
        self._init_connect_recent_list()

    def _init_program(self):
        make_dir(self.app_info.user_path)

    def _init_connect_menu(self):
        self._init_label_logo()
        self._init_button_new()
        self._init_button_open()
        self._init_button_exit()
        self._init_label_name()

    def _init_label_logo(self):
        logo = Picture(str(self.app_info.path / 'logo.png'))
        logo.set_label_widget(self._ui.label_logo_360x160)
        logo.show()

    def _init_button_new(self):
        path = f'{self.app_info.path}/view/start/icons/new_project.png'
        add_icon(self._ui.pushButton_new, path)

        self._ui.pushButton_new.clicked.connect(self.clicked_button_new)
        self._ui.pushButton_new.enterEvent = self.enter_event_button_new
        self._ui.pushButton_new.leaveEvent = self.leave_event_notice_clear

    def enter_event_button_new(self, event):
        self._ui.label_notice.setText('새로운 프로젝트를 생성합니다.')

    def leave_event_notice_clear(self, event):
        self._ui.label_notice.setText('')

    def clicked_button_new(self):
        self.main_view.new_project(parent=self)
        if self.main_view.prj.path:
            self.main_view.show()
            self.recent_list.add_item(str(Path(self.main_view.prj.path).name),
                                      str(self.main_view.prj.path))
            self.close()

    def _init_button_open(self):
        path = f'{self.app_info.path}/view/start/icons/open_project.png'
        add_icon(self._ui.pushButton_open, path)
        
        self._ui.pushButton_open.clicked.connect(self.clicked_button_open)
        self._ui.pushButton_open.enterEvent = self.enter_event_button_open
        self._ui.pushButton_open.leaveEvent =  self.leave_event_notice_clear

    def enter_event_button_open(self, event):
        self._ui.label_notice.setText('저장된 프로젝트를 불러옵니다.')

    def clicked_button_open(self):
        get_path = DirDialogBox.open_folder(self, title='Open Project')
        if get_path:
            self.main_view.set_defaults(get_path)
            self.main_view.show()

            self.recent_list.add_item(str(Path(get_path).name), str(get_path))

            self.close()

    def _init_button_exit(self):
        path = f'{self.app_info.path}/view/start/icons/close_program.png'
        add_icon(self._ui.pushButton_exit, path)
        
        self._ui.pushButton_exit.clicked.connect(self.clicked_button_exit)
        self._ui.pushButton_exit.enterEvent = self.enter_event_button_exit
        self._ui.pushButton_exit.leaveEvent =  self.leave_event_notice_clear

    def enter_event_button_exit(self, event):
        self._ui.label_notice.setText('프로그램을 종료합니다.')

    def clicked_button_exit(self):
        self.close()

    def _init_label_name(self):
        label = self._ui.label_name
        name = "Massive Crowd Simulation 2025, v1.00 beta"
        label.setStyleSheet("font-weight: bold; font-style: italic;")
        label.setText(name)

    def _init_connect_recent_list(self):
        recent_list_layout = self._ui.verticalLayout_recent_list

        self.recent_list = RecentList()
        self.recent_list.set_layout(recent_list_layout)
        self.recent_list.set_func_clicked_item(self.clicked_item_recent_list)
        self.recent_list.set_file_name(Path(rf'{self.app_info.user_path}/recent.json'))

        ui = self.recent_list.get_ui()
        ui.lineEdit_search.enterEvent = self.enter_event_edit_search
        ui.lineEdit_search.leaveEvent = self.leave_event_notice_clear

    def clicked_item_recent_list(self):
        get_path = self.recent_list.selected_path
        get_name = self.recent_list.selected_name
        if is_dir(get_path):
            self.main_view.set_defaults(get_path)
            self.main_view.show()

            self.close()
            self.recent_list.add_item(get_name, get_path)
        else:
            result = messagebox_warning(
                self,
                f'Cannot find path: \n'
                f'[{get_path}]\n\n'
                f'Remove this from recent project list?')
            if result:
                self.recent_list.remove_current_item()

    def enter_event_edit_search(self, event):
        self._ui.label_notice.setText('최근 프로젝트를 검색합니다.')

    def set_defaults(self, open_path=''):
        self.recent_list.set_defaults()

        if open_path:
            self.main_view.set_defaults(open_path)
            self.main_view.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        m = self._shadow_margin
        radius = 14

        # 그림자 (여러 겹으로 부드럽게)
        for i in range(m):
            alpha = int(40 * (1 - i / m))
            spread = m - i
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(
                QRectF(m - spread, m - spread + 1,
                       self.width() - 2 * (m - spread),
                       self.height() - 2 * (m - spread) + 1),
                radius + spread * 0.3, radius + spread * 0.3)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(0, 0, 0, alpha))
            p.drawPath(shadow_path)

        # 본체 배경
        body = QRectF(m, m, self.width() - 2 * m, self.height() - 2 * m)
        body_path = QPainterPath()
        body_path.addRoundedRect(body, radius, radius)
        p.setBrush(QColor(245, 245, 245))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPath(body_path)

        # 테두리
        p.setPen(QPen(QColor(120, 120, 120), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(body_path)

        p.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, '_drag_pos') and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
