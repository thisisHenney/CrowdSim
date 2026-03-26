from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import (QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QMenu, QDialog,
                               QLabel, QPushButton, QTextBrowser, QSlider, QToolButton, QStyleOptionSlider, QStyle)
from PySide6.QtCore import QSize, QSettings, Qt, QTimer
from PySide6.QtGui import QAction


class _ClickSlider(QSlider):
    """클릭한 위치로 바로 이동 + 드래그 가능한 슬라이더"""
    def _pos_to_value(self, pos_x):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        groove = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt,
                                              QStyle.SubControl.SC_SliderGroove, self)
        handle = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt,
                                              QStyle.SubControl.SC_SliderHandle, self)
        slider_len = groove.width() - handle.width()
        offset = groove.x() + handle.width() // 2
        val = self.minimum() + (self.maximum() - self.minimum()) * (pos_x - offset) / max(slider_len, 1)
        return max(self.minimum(), min(self.maximum(), round(val)))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setValue(self._pos_to_value(event.position().x()))
            self._dragging = True
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if getattr(self, '_dragging', False):
            self.setValue(self._pos_to_value(event.position().x()))
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)

from nextlib.utils.ui import load_ui
from nextlib.utils.file import make_dir
from nextlib.dialogbox.dialogbox import DirDialogBox
from nextlib.vtk.vtk_widget_base import VtkWidgetBase
from nextlib.vtk.core.mesh_loader import MeshLoader
from nextlib.widgets.dropdown import DropDown
from nextlib.widgets.tree import TreeWidget
from nextlib.widgets.icon import create_icon
from nextlib.execute.exec_widget import ExecWidget
from nextlib.utils.watcher import DirectoryWatcher
from nextlib.utils.window import center_on_screen

from view.main.main_window_view_ui import Ui_MainWindowView

from view.panel.properties.solver_common_view import SolverCommonView
from view.panel.properties.grid_view import GridView
from view.panel.properties.materials_view import MaterialsView
from view.panel.properties.particle_view import ParticleView
from view.panel.properties.inlet_view import InletView
from view.panel.properties.outlet_view import OutletView
from view.panel.properties.report_view import ReportView
from view.panel.properties.export_view import ExportView

from datarw.e8ight.solver_input import SolverData


@dataclass
class ProjectInfor:
    version: int = 1.00
    path: str = ''
    name: str = 'NoNamed'


class MainWindowView(QMainWindow):
    def __init__(self, app_info):
        super().__init__()

        self.app_info = app_info
        self.prj = ProjectInfor()

        self._ui = load_ui(self, Ui_MainWindowView)

        self.prop_solverCommon = SolverCommonView(self)
        self.prop_grid = GridView(self)
        self.prop_materials = MaterialsView(self)
        self.prop_particle = ParticleView(self)
        self.prop_inlet = InletView(self)
        self.prop_outlet = OutletView(self)
        self.prop_report = ReportView(self)

        self.tree = TreeWidget(widget=self._ui.treeWidget)
        self.vtk = VtkWidgetBase(self)
        # 불필요한 버튼 숨기기
        for attr in ('_action_select_all', '_action_deselect',
                      '_geom_visible_action', '_mesh_visible_action', '_both_visible_action'):
            act = getattr(self.vtk, attr, None)
            if act is not None:
                act.setVisible(False)
        # 툴바 툴팁 항상 표시 (포커스 없어도)
        self.vtk.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        _vtk_frame = QFrame()
        _vtk_frame.setStyleSheet("QFrame { border: 1px solid #d0d7de; border-radius: 4px; background: transparent; }")
        _vtk_layout = QVBoxLayout(_vtk_frame)
        _vtk_layout.setContentsMargins(1, 1, 1, 1)
        _vtk_layout.setSpacing(0)
        _vtk_layout.addWidget(self.vtk)

        self._anim_bar = QFrame()
        self._anim_bar.setFixedHeight(32)
        self._anim_bar.setStyleSheet("QFrame { background: transparent; border: none; border-top: 1px solid #d0d7de; }")
        anim_layout = QHBoxLayout(self._anim_bar)
        anim_layout.setContentsMargins(6, 2, 6, 2)
        anim_layout.setSpacing(4)

        from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QPen, QPolygonF
        from PySide6.QtCore import QPointF

        def _make_anim_icon(draw_func, size=16):
            pix = QPixmap(size, size)
            pix.fill(QColor(0, 0, 0, 0))
            p = QPainter(pix)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(50, 50, 50))
            draw_func(p, size)
            p.end()
            return QIcon(pix)

        def _draw_first(p, s):
            # ◀◀ (last의 반대)
            tri1 = QPolygonF([QPointF(s - 1, 2), QPointF(s - 1, s - 2), QPointF(s / 2, s / 2)])
            p.drawPolygon(tri1)
            tri2 = QPolygonF([QPointF(s / 2, 2), QPointF(s / 2, s - 2), QPointF(1, s / 2)])
            p.drawPolygon(tri2)

        def _draw_prev(p, s):
            # |◀ (next의 반대)
            p.drawRect(1, 2, 2, s - 4)
            tri = QPolygonF([QPointF(s - 2, 2), QPointF(s - 2, s - 2), QPointF(4, s / 2)])
            p.drawPolygon(tri)

        def _draw_play(p, s):
            # ▶
            tri = QPolygonF([QPointF(3, 2), QPointF(3, s - 2), QPointF(s - 3, s / 2)])
            p.drawPolygon(tri)

        def _draw_stop(p, s):
            # ■
            p.drawRect(3, 3, s - 6, s - 6)

        def _draw_next(p, s):
            # ▶|
            tri = QPolygonF([QPointF(2, 2), QPointF(2, s - 2), QPointF(s - 4, s / 2)])
            p.drawPolygon(tri)
            p.drawRect(s - 3, 2, 2, s - 4)

        def _draw_last(p, s):
            # ▶▶
            tri1 = QPolygonF([QPointF(1, 2), QPointF(1, s - 2), QPointF(s / 2, s / 2)])
            p.drawPolygon(tri1)
            tri2 = QPolygonF([QPointF(s / 2, 2), QPointF(s / 2, s - 2), QPointF(s - 1, s / 2)])
            p.drawPolygon(tri2)

        def _draw_reload(p, s):
            # 원형 화살표 (리로드)
            from PySide6.QtGui import QPen
            from PySide6.QtCore import QRectF
            pen = QPen(QColor(50, 50, 50), 2.0)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawArc(QRectF(2, 2, s - 4, s - 4), 60 * 16, 270 * 16)
            # 화살촉
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(50, 50, 50))
            arrow = QPolygonF([QPointF(s / 2 + 1, 1), QPointF(s / 2 + 1, 6), QPointF(s / 2 + 5, 3.5)])
            p.drawPolygon(arrow)

        self._icon_play = _make_anim_icon(_draw_play)
        self._icon_stop = _make_anim_icon(_draw_stop)

        _btn_style = ('QToolButton { border: 1px solid #ccc; border-radius: 3px; background: white; }'
                      ' QToolButton:hover { background: #e8e8e8; }')

        self._btn_anim_reload = QToolButton()
        self._btn_anim_reload.setIcon(_make_anim_icon(_draw_reload))
        self._btn_anim_reload.setToolTip('결과 다시 읽기')
        self._btn_anim_reload.setFixedSize(28, 24)
        self._btn_anim_reload.setStyleSheet(_btn_style)
        self._btn_anim_reload.clicked.connect(self._anim_reload)

        self._btn_anim_first = QToolButton()
        self._btn_anim_first.setIcon(_make_anim_icon(_draw_first))
        self._btn_anim_first.setToolTip('처음으로')
        self._btn_anim_first.setFixedSize(28, 24)
        self._btn_anim_first.setStyleSheet(_btn_style)
        self._btn_anim_first.clicked.connect(self._anim_first)

        self._btn_anim_prev = QToolButton()
        self._btn_anim_prev.setIcon(_make_anim_icon(_draw_prev))
        self._btn_anim_prev.setToolTip('이전 프레임')
        self._btn_anim_prev.setFixedSize(28, 24)
        self._btn_anim_prev.setStyleSheet(_btn_style)
        self._btn_anim_prev.clicked.connect(self._anim_prev)

        self._btn_anim_play = QToolButton()
        self._btn_anim_play.setIcon(self._icon_play)
        self._btn_anim_play.setToolTip('재생 / 정지')
        self._btn_anim_play.setFixedSize(28, 24)
        self._btn_anim_play.setStyleSheet(_btn_style)
        self._btn_anim_play.clicked.connect(self._anim_play_pause)

        self._btn_anim_next = QToolButton()
        self._btn_anim_next.setIcon(_make_anim_icon(_draw_next))
        self._btn_anim_next.setToolTip('다음 프레임')
        self._btn_anim_next.setFixedSize(28, 24)
        self._btn_anim_next.setStyleSheet(_btn_style)
        self._btn_anim_next.clicked.connect(self._anim_next)

        self._btn_anim_last = QToolButton()
        self._btn_anim_last.setIcon(_make_anim_icon(_draw_last))
        self._btn_anim_last.setToolTip('끝으로')
        self._btn_anim_last.setFixedSize(28, 24)
        self._btn_anim_last.setStyleSheet(_btn_style)
        self._btn_anim_last.clicked.connect(self._anim_last)

        self._anim_slider = _ClickSlider(Qt.Orientation.Horizontal)
        self._anim_slider.setMinimum(0)
        self._anim_slider.setMaximum(0)
        self._anim_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._anim_slider.setTickInterval(1)  # _scan_vtk_results에서 재설정
        self._anim_slider.setStyleSheet(
            'QSlider::groove:horizontal {'
            '  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,'
            '    stop:0 #b0c4de, stop:1 #dce6f0);'
            '  height: 6px;'
            '  border-radius: 3px;'
            '}'
            'QSlider::sub-page:horizontal {'
            '  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,'
            '    stop:0 #4a90d9, stop:1 #6aace0);'
            '  height: 6px;'
            '  border-radius: 3px;'
            '}'
            'QSlider::handle:horizontal {'
            '  background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,'
            '    fx:0.4, fy:0.4, stop:0 #ffffff, stop:1 #4a90d9);'
            '  width: 14px;'
            '  height: 14px;'
            '  margin: -5px 0;'
            '  border-radius: 7px;'
            '  border: 1px solid #3a7abd;'
            '}'
            'QSlider::handle:horizontal:hover {'
            '  background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,'
            '    fx:0.4, fy:0.4, stop:0 #ffffff, stop:1 #3a7abd);'
            '  border: 1px solid #2a5a9d;'
            '}'
            'QSlider::tick-mark:horizontal {'
            '  background: #888;'
            '  width: 1px;'
            '  height: 6px;'
            '}')
        self._anim_slider.valueChanged.connect(self._anim_slider_changed)

        from PySide6.QtWidgets import QSpinBox
        self._anim_spin = QSpinBox()
        self._anim_spin.setMinimum(0)
        self._anim_spin.setMaximum(0)
        self._anim_spin.setFixedWidth(60)
        self._anim_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._anim_spin.setStyleSheet('font-size: 11px;')
        self._anim_spin.valueChanged.connect(self._anim_spin_changed)
        self._anim_total_label = QLabel('/ 0')
        self._anim_total_label.setFixedWidth(45)
        self._anim_total_label.setStyleSheet('font-size: 11px;')

        anim_layout.addWidget(self._btn_anim_reload)
        anim_layout.addWidget(self._btn_anim_first)
        anim_layout.addWidget(self._btn_anim_prev)
        anim_layout.addWidget(self._btn_anim_play)
        anim_layout.addWidget(self._btn_anim_next)
        anim_layout.addWidget(self._btn_anim_last)
        self._btn_anim_record = QToolButton()
        self._btn_anim_record.setToolTip('동영상 저장')
        self._btn_anim_record.setFixedSize(28, 24)
        _rec_pix = QPixmap(16, 16)
        _rec_pix.fill(QColor(0, 0, 0, 0))
        _rp = QPainter(_rec_pix)
        _rp.setRenderHint(QPainter.RenderHint.Antialiasing)
        _rp.setPen(Qt.PenStyle.NoPen)
        _rp.setBrush(QColor(240, 150, 30))
        _rp.drawEllipse(1, 1, 14, 14)
        _rp.end()
        self._btn_anim_record.setIcon(QIcon(_rec_pix))
        self._btn_anim_record.setStyleSheet(_btn_style)
        self._btn_anim_record.clicked.connect(self._anim_export_video)

        from PySide6.QtWidgets import QComboBox
        self._anim_speed_combo = QComboBox()
        self._anim_speed_combo.addItems(['x1', 'x1.5', 'x2', 'x4', 'x8', 'x16', 'x32', 'x64'])
        self._anim_speed_combo.setFixedWidth(55)
        self._anim_speed_combo.setToolTip('재생 속도')
        self._anim_speed_combo.setStyleSheet('font-size: 11px;')
        self._anim_speed_combo.currentIndexChanged.connect(self._anim_speed_changed)
        self._anim_speed_ms = 200  # 기본 x1 = 200ms

        anim_layout.addWidget(self._anim_slider, 1)
        anim_layout.addWidget(self._anim_spin)
        anim_layout.addWidget(self._anim_total_label)
        anim_layout.addWidget(self._anim_speed_combo)
        anim_layout.addWidget(self._btn_anim_record)

        _vtk_layout.addWidget(self._anim_bar)
        self._anim_bar.setVisible(False)

        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_timer = QTimer()
        self._anim_timer.timeout.connect(self._anim_tick)
        self._anim_playing = False

        self._ui.verticalLayout_vtk.addWidget(_vtk_frame)
        self._mesh_loader = MeshLoader()
        self.cmd = ExecWidget(self)
        self.properties = DropDown(self._ui.verticalLayout_properties)

        self.solver_watcher = None
        self._solver_proc = None

        self._initialize()

    def _initialize(self):
        self.cmd.put_in_layout(self._ui.verticalLayout_command)
        self.cmd.connect_to_statusbar(self._ui.statusbar)

        self.tree.itemSelectedWithPos.connect(lambda pos, col: self._changed_selection_item())

        self._init_toolbar()
        self._init_menu_connections()

        self.resize(1400, 960)
        # 마우스가 있는 모니터 중앙에 배치
        from PySide6.QtGui import QCursor
        from PySide6.QtWidgets import QApplication
        cursor_pos = QCursor.pos()
        for screen in QApplication.screens():
            if screen.geometry().contains(cursor_pos):
                geo = screen.availableGeometry()
                self.move(geo.x() + (geo.width() - self.width()) // 2,
                          geo.y() + (geo.height() - self.height()) // 2)
                break
        self._restore_window_state()

        # 초기 카메라: X 오른쪽, Y 위쪽, Z 모니터 앞쪽
        cam = self.vtk.renderer.GetActiveCamera()
        cam.SetPosition(0, 0, 1)
        cam.SetFocalPoint(0, 0, 0)
        cam.SetViewUp(0, 1, 0)
        self.vtk.renderer.ResetCamera()

        self.setWindowTitle(f'{self.app_info.title}-{self.app_info.version}')

    def _init_menu_connections(self):
        self._ui.actionNew_Projcect.triggered.connect(self.new_project)
        self._ui.actionOpen_Project.triggered.connect(self.open_project)
        self._ui.actionSave_Projcet.triggered.connect(self.save)
        self._ui.actionSave_As_Project.triggered.connect(self._save_as_project)
        self._ui.actionClose_Project.setVisible(False)
        self._ui.actionExit.triggered.connect(self.close)

        self._recent_menu = QMenu(self)
        self._ui.actionRecent_Project.setMenu(self._recent_menu)
        self._refresh_recent_menu()

        self._ui.actionProperties.setVisible(False)

        self._ui.menuSolver.menuAction().setVisible(False)
        self._ui.menuAnalysis.menuAction().setVisible(False)
        self._ui.menuCrowd.menuAction().setVisible(False)
        self._ui.menuReport.menuAction().setVisible(False)

        self._ui.actionSetting.triggered.connect(
            lambda: self._ui.dockWidget_settings.setVisible(not self._ui.dockWidget_settings.isVisible()))
        self._ui.actionProperties_2.triggered.connect(
            lambda: self._ui.dockWidget_properties.setVisible(not self._ui.dockWidget_properties.isVisible()))
        self._ui.actionCommand.triggered.connect(
            lambda: self._ui.dockWidget_command.setVisible(not self._ui.dockWidget_command.isVisible()))

        self._tools_menu = QMenu('Tools', self)
        self._ui.menubar.insertMenu(self._ui.menuHelp.menuAction(), self._tools_menu)

        action_open_folder = self._tools_menu.addAction('케이스 폴더 열기')
        action_open_folder.triggered.connect(self._open_case_folder)

        action_open_terminal = self._tools_menu.addAction('터미널 열기')
        action_open_terminal.triggered.connect(self._open_terminal)

        self._ui.actionHelp.triggered.connect(self._open_manual)
        self._ui.actionAbout.triggered.connect(self._open_about)

    def _save_as_project(self):
        get_path = DirDialogBox.open_folder(self, title='Save As - 저장할 폴더 선택')
        if get_path:
            self.prj.path = get_path
            self.prj.name = Path(get_path).name
            self.setWindowTitle(f'{self.app_info.title} - [{self.prj.path}]')
            self.save_input_file()

    def _close_project(self):
        self.tree.clear_all()
        self.properties.set_defaults()
        self.vtk.obj_manager.all().remove()
        self.prj = ProjectInfor()
        self.setWindowTitle(f'{self.app_info.title}-{self.app_info.version}')

    def _load_recent_projects(self):
        recent = self._settings().value('recentProjects', [])
        if isinstance(recent, str):
            recent = [recent]
        return [p for p in (recent or []) if Path(p).is_dir()]

    def _add_recent_project(self, path):
        recent = self._load_recent_projects()
        path = str(path)
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        self._settings().setValue('recentProjects', recent[:10])
        self._refresh_recent_menu()

    def _refresh_recent_menu(self):
        self._recent_menu.clear()
        recent = self._load_recent_projects()
        if recent:
            for path in recent:
                action = self._recent_menu.addAction(path)
                action.setToolTip(path)
                action.triggered.connect(lambda checked, p=path: self.set_defaults(p))
            self._recent_menu.addSeparator()
            clear_action = self._recent_menu.addAction('목록 지우기')
            clear_action.triggered.connect(self._clear_recent_projects)
        else:
            empty = self._recent_menu.addAction('(최근 항목 없음)')
            empty.setEnabled(False)

    def _open_case_folder(self):
        if not self.prj.path:
            return
        import os
        os.startfile(self.prj.path)

    def _open_terminal(self):
        if not self.prj.path:
            return
        import subprocess
        subprocess.Popen('cmd', cwd=str(self.prj.path),
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

    def _clear_recent_projects(self):
        self._settings().setValue('recentProjects', [])
        self._refresh_recent_menu()

    def _open_manual(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Manual')
        dlg.resize(560, 480)
        layout = QVBoxLayout(dlg)

        browser = QTextBrowser()
        browser.setHtml("""
        <h2 style="color:#2a6eba;">Massive Crowd Simulation 사용 매뉴얼</h2>
        <hr>
        <h3>1. 프로젝트 관리</h3>
        <ul>
          <li><b>File &gt; New</b>: 새 프로젝트 폴더를 생성합니다.</li>
          <li><b>File &gt; Open</b>: 기존 프로젝트 폴더를 엽니다.</li>
          <li><b>File &gt; Recent</b>: 최근 열었던 프로젝트를 빠르게 엽니다.</li>
          <li><b>File &gt; Save / Save As</b>: 현재 설정을 JSON 파일로 저장합니다.</li>
          <li><b>File &gt; Close</b>: 현재 프로젝트를 닫습니다.</li>
        </ul>
        <h3>2. 설정 패널 (우측)</h3>
        <ul>
          <li><b>해석 일반 (Solver)</b>: 시뮬레이션 시간, 스텝 등 기본 설정</li>
          <li><b>Grid</b>: 격자 크기 및 해상도 설정</li>
          <li><b>Materials</b>: 재질 물성 설정</li>
          <li><b>Particle Generation</b>: 파티클 생성 영역 및 세그먼트 설정</li>
          <li><b>Inlet</b>: 군중 유입 조건 설정</li>
          <li><b>Outlet</b>: 군중 유출 조건 설정</li>
          <li><b>Report</b>: 결과 출력 설정</li>
        </ul>
        <h3>3. 해석 실행</h3>
        <ul>
          <li>툴바 <b>Run</b> 버튼: 설정을 저장하고 솔버를 실행합니다.</li>
          <li>툴바 <b>Stop</b> 버튼: 실행 중인 솔버를 중단합니다.</li>
          <li>하단 <b>Command 패널</b>에서 실행 로그를 확인합니다.</li>
          <li>해석 결과는 VTK 뷰포트에 실시간으로 표시됩니다.</li>
        </ul>
        <h3>4. 화면 구성</h3>
        <ul>
          <li><b>Window &gt; Setting</b>: 좌측 트리 패널 표시/숨김</li>
          <li><b>Window &gt; Properties</b>: 우측 설정 패널 표시/숨김</li>
          <li><b>Window &gt; Command</b>: 하단 로그 패널 표시/숨김</li>
          <li>각 패널은 드래그로 위치를 변경할 수 있으며, 재시작 시 자동 복원됩니다.</li>
        </ul>
        """)
        layout.addWidget(browser)

        close_btn = QPushButton('닫기')
        close_btn.setFixedHeight(32)
        close_btn.clicked.connect(dlg.accept)
        layout.addWidget(close_btn)
        dlg.exec()

    def _open_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('About')
        dlg.setFixedSize(360, 240)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(6)
        layout.setContentsMargins(24, 24, 24, 16)

        title_lbl = QLabel(self.app_info.title)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet('font-size: 15px; font-weight: bold;')

        version_lbl = QLabel(f'Version  {self.app_info.version}')
        version_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_lbl.setStyleSheet('color: #666; font-size: 12px;')

        desc_lbl = QLabel('대규모 군중 시뮬레이션 솔루션\nⓒ NEXTfoam Co., Ltd.')
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setStyleSheet('color: #888; font-size: 11px;')

        layout.addStretch()
        layout.addWidget(title_lbl)
        layout.addWidget(version_lbl)
        layout.addSpacing(10)
        layout.addWidget(desc_lbl)
        layout.addStretch()

        ok_btn = QPushButton('확인')
        ok_btn.setFixedHeight(32)
        ok_btn.clicked.connect(dlg.accept)
        layout.addWidget(ok_btn)
        dlg.exec()

    def _init_toolbar(self):
        self._icon_path = self.app_info.path / 'view/main/icons'
        self._ui.toolBar.setIconSize(QSize(32, 32))

        self.action_file_new = QAction(create_icon(str(self._icon_path / 'new.png')), 'New', self)
        self._ui.toolBar.addAction(self.action_file_new)

        self.action_file_open = QAction(create_icon(str(self._icon_path / 'open.png')), 'Open', self)
        self._ui.toolBar.addAction(self.action_file_open)

        self.action_file_save = QAction(create_icon(str(self._icon_path / 'save.png')), 'Save', self)
        self._ui.toolBar.addAction(self.action_file_save)

        self._ui.toolBar.addSeparator()

        self.action_run = QAction(create_icon(str(self._icon_path / 'run.png')), 'Run', self)
        self._ui.toolBar.addAction(self.action_run)

        self.action_stop = QAction(create_icon(str(self._icon_path / 'stop.png')), 'Stop', self)
        self.action_stop.setEnabled(False)
        self._ui.toolBar.addAction(self.action_stop)

        self._ui.toolBar.addSeparator()

        # 배경 이미지 로드 버튼 (QPainter로 아이콘 생성)
        from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QPen, QPolygonF
        from PySide6.QtCore import QRectF, QPointF
        _bg_pix = QPixmap(32, 32)
        _bg_pix.fill(QColor(0, 0, 0, 0))
        _bgp = QPainter(_bg_pix)
        _bgp.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 산 모양
        _bgp.setPen(QPen(QColor(60, 120, 60), 2))
        _bgp.setBrush(QColor(100, 180, 100))
        _bgp.drawPolygon(QPolygonF([QPointF(2, 26), QPointF(12, 8), QPointF(22, 26)]))
        _bgp.drawPolygon(QPolygonF([QPointF(14, 26), QPointF(24, 12), QPointF(30, 26)]))
        # 태양
        _bgp.setPen(Qt.PenStyle.NoPen)
        _bgp.setBrush(QColor(255, 200, 50))
        _bgp.drawEllipse(22, 2, 8, 8)
        _bgp.end()
        self.action_bg_map = QAction(QIcon(_bg_pix), '배경 이미지', self)
        self.action_bg_map.setToolTip('배경 지도 이미지 불러오기')
        self._ui.toolBar.addAction(self.action_bg_map)

        self._ui.toolBar.actionTriggered.connect(self._clicked_toolbar_button)

    def _clicked_toolbar_button(self, action):
        if action == self.action_file_new:
            self.new_project()
        elif action == self.action_file_open:
            self.open_project()
        elif action == self.action_file_save:
            self.save()
        elif action == self.action_run:
            self.run_solver()
        elif action == self.action_stop:
            self.stop_solver()
        elif action == self.action_bg_map:
            self._select_background_map()

    def _select_background_map(self):
        """사용자가 배경 이미지를 선택하여 케이스 map/ 폴더에 복사 후 로드"""
        from PySide6.QtWidgets import QFileDialog
        import shutil
        filepath, _ = QFileDialog.getOpenFileName(
            self, '배경 지도 이미지 선택', '',
            '이미지 파일 (*.jpg *.jpeg *.png *.bmp);;All Files (*)')
        if not filepath:
            return
        # 케이스 map/ 폴더에 복사
        if self.prj.path:
            map_dir = Path(self.prj.path) / 'map'
            map_dir.mkdir(parents=True, exist_ok=True)
            dest = map_dir / Path(filepath).name
            if str(Path(filepath).resolve()) != str(dest.resolve()):
                shutil.copy2(filepath, dest)
            self._bg_map_path = str(dest)
        else:
            self._bg_map_path = filepath
        self._load_background_map(self._bg_map_path)

    def set_defaults(self, path):
        self.prj.path = path
        self.prj.name = Path(self.prj.path).name

        self._add_recent_project(path)

        self.set_defaults_tree()
        self.cmd.set_defaults()
        self.set_defaults_vtk()
        self.set_defaults_properties()
        self.load_input_file()
        self._load_background_map()
        self._scan_vtk_results()

        self.setWindowTitle(f'{self.app_info.title} - [{self.prj.path}]')
        self._ui.statusbar.showMessage('Ready')

        self.show()

    def set_defaults_tree(self):
        self.tree.clear_all()

        self.tree.insert([0], 'Solver')

        self.tree.insert([1], 'Grid')
        self.tree.insert([2], 'Materials')
        self.tree.insert([3], 'Particle Generation')
        self.tree.insert([4], 'Inlet')
        self.tree.insert([5], 'Outlet')
        self.tree.insert([6], 'Report&Export')

    def _changed_selection_item(self):
        pos = self.tree.get_current_pos()
        if not pos:
            return

        if len(pos) == 1:
            self.properties.open_item(pos[0])

        else:
            return

    def set_defaults_vtk(self):
        # 프리로드 중이면 중단
        if hasattr(self, '_preload_timer') and self._preload_timer is not None:
            self._preload_timer.stop()
            self._preload_timer = None
        # 기존 VTK 객체 모두 제거
        self.vtk.obj_manager.all().remove()
        # 배경 맵 제거
        if hasattr(self, '_bg_map_actor') and self._bg_map_actor is not None:
            self.vtk.renderer.RemoveActor(self._bg_map_actor)
            self._bg_map_actor = None
        if hasattr(self, '_bg_overlay_actor') and self._bg_overlay_actor is not None:
            self.vtk.renderer.RemoveActor(self._bg_overlay_actor)
            self._bg_overlay_actor = None
        # 애니메이션 상태 초기화
        self._anim_stop_play()
        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_slider.setValue(0)
        self._anim_slider.setMaximum(0)
        self._anim_spin.blockSignals(True)
        self._anim_spin.setMaximum(0)
        self._anim_spin.setValue(0)
        self._anim_spin.blockSignals(False)
        self._anim_total_label.setText('/ 0')
        self._anim_bar.setVisible(False)
        self.vtk.vtk_widget.GetRenderWindow().Render()

    def set_defaults_properties(self):
        self.properties.set_defaults()

        self.properties.insert_item(0, '해석 일반', self.prop_solverCommon.get_widget())

        self.properties.insert_item(1, 'Grid', self.prop_grid.get_widget())
        self.properties.insert_item(2, 'Materials', self.prop_materials.get_widget())

        self.properties.insert_item(3, 'Particle', self.prop_particle.get_widget())
        self.properties.insert_item(4, 'Inlet', self.prop_inlet.get_widget())
        self.properties.insert_item(5, 'Outlet', self.prop_outlet.get_widget())

        self.properties.insert_item(6, 'Report', self.prop_report.get_widget())

    def new_project(self, parent=None):
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                        QLabel, QLineEdit, QPushButton, QFileDialog)

        dlg = QDialog(parent or self)
        dlg.setWindowTitle('새 프로젝트')
        dlg.setFixedWidth(450)
        layout = QVBoxLayout(dlg)

        # 최근 경로 불러오기 (없으면 바탕화면)
        import json
        _settings_file = self.app_info.user_path / 'CrowdSim' / 'settings.json'
        _app_settings = {}
        if _settings_file.exists():
            try:
                _app_settings = json.loads(_settings_file.read_text(encoding='utf-8'))
            except Exception:
                pass
        # 바탕화면 경로 (Windows API로 실제 경로 가져오기)
        _default_path = str(Path.home() / 'Desktop')
        try:
            import ctypes
            _buf = ctypes.create_unicode_buffer(260)
            ctypes.windll.shell32.SHGetFolderPathW(None, 0x0000, None, 0, _buf)
            if _buf.value:
                _default_path = _buf.value
        except Exception:
            pass
        last_path = _app_settings.get('new_project_last_path', _default_path)

        # 경로 선택
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel('경로:'))
        path_edit = QLineEdit()
        path_edit.setText(last_path)
        path_edit.setReadOnly(True)
        path_row.addWidget(path_edit, 1)
        btn_browse = QPushButton('찾아보기')
        def _browse_path():
            selected = QFileDialog.getExistingDirectory(dlg, '프로젝트 경로 선택', path_edit.text())
            if selected:
                path_edit.setText(str(Path(selected).resolve()))
        btn_browse.clicked.connect(_browse_path)
        path_row.addWidget(btn_browse)
        layout.addLayout(path_row)

        # 케이스 이름 입력
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel('이름:'))
        name_edit = QLineEdit()
        name_edit.setPlaceholderText('케이스 이름을 입력하세요')
        name_row.addWidget(name_edit, 1)
        layout.addLayout(name_row)

        # 버튼
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_ok = QPushButton('생성')
        btn_ok.setDefault(True)
        btn_cancel = QPushButton('취소')
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        btn_cancel.clicked.connect(dlg.reject)
        btn_ok.clicked.connect(dlg.accept)

        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        base_path = path_edit.text().strip()
        case_name = name_edit.text().strip()
        if not base_path or not case_name:
            return

        # 최근 경로 저장
        _app_settings['new_project_last_path'] = base_path
        _settings_file.parent.mkdir(parents=True, exist_ok=True)
        _settings_file.write_text(json.dumps(_app_settings, ensure_ascii=False, indent=2), encoding='utf-8')

        get_path = str(Path(base_path) / case_name)

        make_dir(get_path)
        make_dir(f'{get_path}/map')

        self.set_defaults(get_path)

    def open_project(self):
        get_path = DirDialogBox.open_folder(self, title='Open Project')
        if get_path:
            self.set_defaults(get_path)

    def load_input_file(self):
        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
        if not json_path.is_file():
            return

        solver = SolverData()
        solver.load(json_path)

        self.prop_solverCommon.load_input_file(solver)
        self.prop_grid.load_input_file(solver)
        self.prop_materials.load_input_file(solver)
        self.prop_particle.load_input_file(solver)
        self.prop_inlet.load_input_file(solver)
        self.prop_outlet.load_input_file(solver)
        self.prop_report.load_input_file(solver)

    def save(self):
        self.save_input_file()

    def _settings(self):
        ini_path = self.app_info.user_path / 'CrowdSim' / 'window_state.ini'
        ini_path.parent.mkdir(parents=True, exist_ok=True)
        return QSettings(str(ini_path), QSettings.Format.IniFormat)

    def _save_window_state(self):
        s = self._settings()
        s.setValue('geometry', self.saveGeometry())
        s.setValue('windowState', self.saveState())
        s.setValue('splitter', self._ui.splitter.saveState())

    def _restore_window_state(self):
        s = self._settings()
        geometry = s.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        state = s.value('windowState')
        if state:
            self.restoreState(state)
        splitter = s.value('splitter')
        if splitter:
            self._ui.splitter.restoreState(splitter)

    def end(self):
        if self.solver_watcher is not None and self.solver_watcher.is_watching():
            self.solver_watcher.end()

    def closeEvent(self, e):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, '종료 확인', '프로그램을 종료하시겠습니까?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self._save_window_state()
            self.end()
            e.accept()
        else:
            e.ignore()

    def run_solver(self):
        import subprocess
        import threading
        import queue
        self.save_input_file()
        self.vtk.obj_manager.all().remove()

        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_playing = False
        self._anim_timer.stop()
        self._anim_slider.setValue(0)
        self._anim_slider.setMaximum(0)
        self._anim_spin.blockSignals(True)
        self._anim_spin.setMaximum(0)
        self._anim_spin.setValue(0)
        self._anim_spin.blockSignals(False)
        self._anim_total_label.setText('/ 0')
        self._anim_bar.setVisible(False)

        self._load_background_map()

        solver_exe = str(self.app_info.path / 'solver/e8ight/RuntimeSPH2D/RuntimeSPH2D.exe')
        json_rel = f'.\\{self.prj.name}.json'
        working_path = str(self.prj.path)

        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE: 콘솔 창 숨김

        self._solver_proc = subprocess.Popen(
            [solver_exe, json_rel],
            cwd=working_path,
            startupinfo=si,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        self.cmd.add_log_notice(f'Solver started: {self.prj.name}.json')
        self.action_run.setEnabled(False)
        self.action_stop.setEnabled(True)
        self._solver_output_buf = ''

        combo = self.cmd._ui.comboBox_output_proc_index
        self._console_combo_index = combo.count()
        combo.addItem('Console')
        try:
            combo.currentIndexChanged.disconnect(self._on_output_combo_changed)
        except RuntimeError:
            pass
        combo.currentIndexChanged.connect(self._on_output_combo_changed)
        combo.setCurrentIndex(self._console_combo_index)

        # 백그라운드 스레드에서 stdout 읽기
        self._solver_queue = queue.Queue()
        self._solver_reader = threading.Thread(
            target=self._read_solver_stdout, daemon=True)
        self._solver_reader.start()

        from PySide6.QtCore import QTimer
        self._solver_timer = QTimer()
        self._solver_timer.timeout.connect(self._poll_solver_output)
        self._solver_timer.start(300)

        output_dir = Path(rf'{self.prj.path}/{self.prj.name}')
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.solver_watcher is not None:
            self.solver_watcher.end()
        self.solver_watcher = DirectoryWatcher()
        self.solver_watcher.start(output_dir)
        self.solver_watcher.changed.connect(self.update_solver_file)

    def _read_solver_stdout(self):
        """백그라운드 스레드: solver stdout을 한 줄씩 읽어서 큐에 넣음"""
        try:
            for raw_line in self._solver_proc.stdout:
                if isinstance(raw_line, bytes):
                    line = raw_line.decode('utf-8', errors='replace')
                else:
                    line = raw_line
                self._solver_queue.put(line.rstrip('\n\r'))
        except Exception:
            pass
        self._solver_queue.put(None)  # sentinel: stdout 닫힘

    def _on_output_combo_changed(self, index):
        if index == getattr(self, '_console_combo_index', -1):
            from PySide6.QtCore import QTimer
            QTimer.singleShot(50, self._restore_console_output)

    def _restore_console_output(self):
        buf = getattr(self, '_solver_output_buf', '')
        if buf:
            self.cmd._output_view.setPlainText(buf)
            scrollbar = self.cmd._output_view.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def _update_solver_output(self, new_text):
        from PySide6.QtGui import QTextCursor
        self._solver_output_buf += new_text
        self.cmd._output_view.moveCursor(QTextCursor.MoveOperation.End)
        self.cmd._output_view.insertPlainText(new_text)
        scrollbar = self.cmd._output_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _poll_solver_output(self):
        import re
        import queue

        if not self._solver_proc:
            self._solver_timer.stop()
            return

        # 큐에서 새 출력 라인 읽기
        stdout_closed = False
        while True:
            try:
                line = self._solver_queue.get_nowait()
            except queue.Empty:
                break
            if line is None:
                stdout_closed = True
                break
            clean = re.sub(r'\x1b\[[0-9;]*m', '', line)
            if clean.strip():
                self._update_solver_output(clean + '\n')

        # 프로세스 종료 확인
        if self._solver_proc.poll() is not None or stdout_closed:
            self._solver_timer.stop()
            # 남은 출력 drain
            while True:
                try:
                    line = self._solver_queue.get_nowait()
                except queue.Empty:
                    break
                if line is None:
                    break
                clean = re.sub(r'\x1b\[[0-9;]*m', '', line)
                if clean.strip():
                    self._update_solver_output(clean + '\n')

            try:
                self._solver_proc.wait(timeout=3)
            except Exception:
                pass
            exit_code = self._solver_proc.returncode
            if exit_code is not None and exit_code == 0:
                self.cmd.add_log_notice('Solver completed')
            elif exit_code is not None:
                self.cmd.add_log_error(0, f'Solver stopped (exit code: {exit_code})')
            else:
                self.cmd.add_log_notice('Solver finished')
            self._solver_proc = None
            self.action_run.setEnabled(True)
            self.action_stop.setEnabled(False)
            if self.solver_watcher is not None:
                self.solver_watcher.end()
                self.solver_watcher = None
            if hasattr(self, '_solver_watcher2') and self._solver_watcher2 is not None:
                self._solver_watcher2.end()
                self._solver_watcher2 = None

    def save_input_file(self):
        solver = SolverData()
        solver.create(Path(rf'{self.prj.path}/{self.prj.name}.json'))
        solver.save()

        solver = self.prop_solverCommon.save_input_file(solver)
        solver.save()
        solver = self.prop_grid.save_input_file(solver)
        solver.save()
        solver = self.prop_materials.save_input_file(solver)
        solver.save()
        solver = self.prop_particle.save_input_file(solver)
        solver.save()
        solver = self.prop_inlet.save_input_file(solver)
        solver.save()
        solver = self.prop_outlet.save_input_file(solver)
        solver.save()
        solver = self.prop_report.save_input_file(solver)
        solver.save()

    def update_solver_file(self, file_name, added_files, removed_files):
        import re
        if not added_files:
            return

        for recent_file in added_files:
            if not recent_file.endswith('.vtk'):
                continue

            match = re.search(r'_grid(\d+)_(\d+)\.vtk$', recent_file)
            if not match:
                continue

            grid_num = int(match.group(1))
            step = int(match.group(2))

            if step not in self._anim_files:
                self._anim_files[step] = {}
            self._anim_files[step][grid_num] = recent_file

            if step not in self._anim_steps:
                self._anim_steps.append(step)
                self._anim_steps.sort()
                total = len(self._anim_steps)
                self._anim_slider.setMaximum(total - 1)
                self._anim_slider.setTickInterval(max(1, total // 2))
                self._anim_spin.setMaximum(total)
                self._anim_total_label.setText(f'/ {total}')
                self._anim_bar.setVisible(True)

        if self._anim_steps:
            last_idx = len(self._anim_steps) - 1
            if self._anim_slider.value() == last_idx:
                # 같은 값이면 시그널 안 나오므로 직접 호출
                self._anim_show_step(last_idx)
            else:
                self._anim_slider.setValue(last_idx)

    def stop_solver(self):
        if hasattr(self, '_solver_timer') and self._solver_timer:
            self._solver_timer.stop()

        if hasattr(self, '_solver_proc') and self._solver_proc and self._solver_proc.poll() is None:
            import subprocess
            pid = self._solver_proc.pid
            # 프로세스 트리 강제 종료
            try:
                subprocess.call(
                    ['taskkill', '/F', '/T', '/PID', str(pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                try:
                    self._solver_proc.kill()
                except Exception:
                    pass
            try:
                self._solver_proc.wait(timeout=5)
            except Exception:
                pass
            self._solver_proc = None
            self.cmd.add_log_notice('Solver stopped by user')
            self.action_run.setEnabled(True)
            self.action_stop.setEnabled(False)

        if self.solver_watcher is not None:
            self.solver_watcher.end()
            self.solver_watcher = None

    def _load_background_map(self, image_path=None):
        """배경 지도 이미지를 VTK 렌더러에 로드"""
        import vtk

        if image_path:
            map_file = Path(image_path)
        elif hasattr(self, '_bg_map_path') and self._bg_map_path:
            map_file = Path(self._bg_map_path)
        else:
            map_file = None
            # 1순위: 케이스 폴더의 map/ 에서 탐색
            if self.prj.path:
                case_map_dir = Path(self.prj.path) / 'map'
                if case_map_dir.is_dir():
                    for ext in ('*.jpg', '*.jpeg', '*.png', '*.bmp'):
                        files = list(case_map_dir.glob(ext))
                        if files:
                            map_file = files[0]
                            break
            # 2순위: resource/map 폴더 (fallback)
            if map_file is None:
                res_map_dir = Path(__file__).resolve().parent.parent.parent / 'resource' / 'map'
                for ext in ('*.jpg', '*.jpeg', '*.png'):
                    files = list(res_map_dir.glob(ext))
                    if files:
                        map_file = files[0]
                        break

        if map_file is None or not Path(map_file).exists():
            return

        # Grid 패널에서 domain 직접 읽기
        d_min = d_max = None
        if hasattr(self, 'prop_grid') and self.prop_grid.grid_data:
            gd = self.prop_grid.grid_data[0]
            try:
                d_min = [float(gd.domain_min[0]), float(gd.domain_min[1])]
                d_max = [float(gd.domain_max[0]), float(gd.domain_max[1])]
            except (ValueError, IndexError):
                pass

        # Grid 데이터 없으면 JSON에서 fallback
        if d_min is None or d_max is None:
            json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
            if not json_path.is_file():
                return
            solver = SolverData()
            solver.load(json_path)
            grids = solver.data.get('config.grid')
            if not grids or len(grids) == 0:
                return
            domain = grids[0].get('domain', {})
            d_min = domain.get('min', [-155, -125, 1])[:2]
            d_max = domain.get('max', [210, 165, 1])[:2]

        suffix = Path(map_file).suffix.lower()
        if suffix in ('.jpg', '.jpeg'):
            reader = vtk.vtkJPEGReader()
        elif suffix == '.bmp':
            reader = vtk.vtkBMPReader()
        else:
            reader = vtk.vtkPNGReader()
        reader.SetFileName(str(map_file))
        reader.Update()

        img_data = reader.GetOutput()
        dims = img_data.GetDimensions()

        plane = vtk.vtkPlaneSource()
        plane.SetOrigin(d_min[0], d_min[1], -0.01)
        plane.SetPoint1(d_max[0], d_min[1], -0.01)
        plane.SetPoint2(d_min[0], d_max[1], -0.01)
        plane.Update()

        texture = vtk.vtkTexture()
        texture.SetInputConnection(reader.GetOutputPort())
        texture.InterpolateOn()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetTexture(texture)

        overlay_plane = vtk.vtkPlaneSource()
        overlay_plane.SetOrigin(d_min[0], d_min[1], -0.005)
        overlay_plane.SetPoint1(d_max[0], d_min[1], -0.005)
        overlay_plane.SetPoint2(d_min[0], d_max[1], -0.005)
        overlay_plane.Update()

        overlay_mapper = vtk.vtkPolyDataMapper()
        overlay_mapper.SetInputConnection(overlay_plane.GetOutputPort())

        overlay_actor = vtk.vtkActor()
        overlay_actor.SetMapper(overlay_mapper)
        overlay_actor.GetProperty().SetColor(0, 0, 0)
        overlay_actor.GetProperty().SetOpacity(0.4)

        if hasattr(self, '_bg_map_actor') and self._bg_map_actor is not None:
            self.vtk.renderer.RemoveActor(self._bg_map_actor)
        if hasattr(self, '_bg_overlay_actor') and self._bg_overlay_actor is not None:
            self.vtk.renderer.RemoveActor(self._bg_overlay_actor)

        self._bg_map_actor = actor
        self._bg_overlay_actor = overlay_actor
        self.vtk.renderer.AddActor(actor)
        self.vtk.renderer.AddActor(overlay_actor)
        self.vtk.renderer.ResetCamera()
        self.vtk.vtk_widget.GetRenderWindow().Render()

    def _scan_vtk_results(self):
        """케이스 열 때 기존 VTK 결과 파일 스캔"""
        import re
        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_playing = False
        self._anim_timer.stop()

        result_dir = Path(self.prj.path) / self.prj.name
        if not result_dir.is_dir():
            self._anim_bar.setVisible(False)
            return

        for vtk_file in result_dir.glob('*.vtk'):
            match = re.search(r'_grid(\d+)_(\d+)\.vtk$', vtk_file.name)
            if not match:
                continue
            grid_num = int(match.group(1))
            step = int(match.group(2))

            if step not in self._anim_files:
                self._anim_files[step] = {}
            self._anim_files[step][grid_num] = str(vtk_file)

        if self._anim_files:
            self._anim_steps = sorted(self._anim_files.keys())
            total = len(self._anim_steps)
            self._anim_slider.setMaximum(total - 1)
            self._anim_slider.setTickInterval(max(1, total // 2))
            self._anim_spin.setMinimum(1)
            self._anim_spin.setMaximum(total)
            self._anim_total_label.setText(f'/ {total}')
            self._anim_slider.setValue(0)
            self._anim_bar.setVisible(True)
            self._anim_show_step(0)
            self._set_2d_view()
            self._anim_preload()
        else:
            self._anim_bar.setVisible(False)

    def _set_2d_view(self):
        """카메라를 3D 퍼스펙티브 뷰로 설정 (X 오른쪽, Y 위쪽, Z 앞쪽)"""
        cam = self.vtk.renderer.GetActiveCamera()
        cam.ParallelProjectionOff()
        cam.SetPosition(0, 0, 1)
        cam.SetFocalPoint(0, 0, 0)
        cam.SetViewUp(0, 1, 0)
        self.vtk.renderer.ResetCamera()
        self.vtk.vtk_widget.GetRenderWindow().Render()

    def _load_vtk_colored_OLD(self, filepath):
        """OLD 2D version - replaced by 3D"""
        import struct
        import math
        import vtk

        with open(filepath, 'rb') as f:
            for _ in range(4):
                f.readline()
            points_line = f.readline().decode('ascii').strip()
            num_points = int(points_line.split()[1])
            points_data = f.read(num_points * 3 * 4)
            rest_bytes = f.read()

        if num_points == 0:
            return None

        vals = struct.unpack(f'>{num_points * 3}f', points_data)
        positions = [(vals[i*3], vals[i*3+1]) for i in range(num_points)]

        velocities = [(0.0, 0.0)] * num_points
        try:
            text = rest_bytes.decode('ascii', errors='replace')
            import re
            field_match = re.search(r'FIELD FieldData (\d+)', text)
            if field_match:
                field_start = text.index('FIELD FieldData')
                header_text = rest_bytes.decode('ascii', errors='replace')
                field_offset = header_text.index('FIELD FieldData')
                cursor = field_offset
                nl = header_text.index('\n', cursor)
                cursor = nl + 1

                type_sizes = {'unsigned_char': 1, 'float': 4, 'int': 4}

                for _ in range(14):
                    nl = header_text.index('\n', cursor)
                    field_line = header_text[cursor:nl].strip()
                    cursor = nl + 1
                    parts = field_line.split()
                    if len(parts) < 4:
                        continue
                    fname, ncomp, ntuples, dtype = parts[0], int(parts[1]), int(parts[2]), parts[3]
                    data_size = ncomp * ntuples * type_sizes.get(dtype, 4)

                    if fname == 'velocity' and ncomp >= 2:
                        vel_bytes = rest_bytes[cursor:cursor + data_size]
                        vel_vals = struct.unpack(f'>{ncomp * ntuples}f', vel_bytes)
                        velocities = [(vel_vals[i*ncomp], vel_vals[i*ncomp+1]) for i in range(ntuples)]

                    cursor += data_size
                    while cursor < len(header_text) and header_text[cursor] == '\n':
                        cursor += 1
        except Exception:
            pass

        S = 1.2

        all_points = vtk.vtkPoints()
        all_lines = vtk.vtkCellArray()
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName('Colors')

        head_points = vtk.vtkPoints()
        head_circles = vtk.vtkCellArray()
        head_colors = vtk.vtkUnsignedCharArray()
        head_colors.SetNumberOfComponents(3)
        head_colors.SetName('Colors')

        pid = 0
        hpid = 0

        for i in range(num_points):
            px, py = positions[i]
            vx, vy = velocities[i]
            speed = math.sqrt(vx*vx + vy*vy)

            if speed > 0.01:
                angle = math.atan2(vy, vx) - math.pi / 2
            else:
                angle = 0.0

            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            def rot(lx, ly):
                """로컬 좌표를 회전 후 월드 좌표로"""
                rx = lx * cos_a - ly * sin_a + px
                ry = lx * sin_a + ly * cos_a + py
                return rx, ry

            hip = rot(0, S * 0.35)
            neck = rot(0, S * 0.75)
            head_center = rot(0, S * 0.88)

            l_hand = rot(-S * 0.25, S * 0.45)
            r_hand = rot(S * 0.25, S * 0.45)

            l_foot = rot(-S * 0.2, 0)
            r_foot = rot(S * 0.2, 0)

            t = min(speed / 2.0, 1.0)
            cr = int(255 * t)
            cg = int(255 * (1 - abs(t - 0.5) * 2))
            cb = int(255 * (1 - t))

            def add_line(p1, p2):
                nonlocal pid
                id1 = all_points.InsertNextPoint(p1[0], p1[1], 0)
                id2 = all_points.InsertNextPoint(p2[0], p2[1], 0)
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, id1)
                line.GetPointIds().SetId(1, id2)
                all_lines.InsertNextCell(line)
                colors.InsertNextTuple3(cr, cg, cb)
                pid += 2

            add_line(hip, neck)
            add_line(neck, l_hand)
            add_line(neck, r_hand)
            add_line(hip, l_foot)
            add_line(hip, r_foot)

            head_r = S * 0.13
            n_seg = 8
            first_hid = None
            for s in range(n_seg):
                a = 2 * math.pi * s / n_seg
                hx = head_center[0] + head_r * math.cos(a)
                hy = head_center[1] + head_r * math.sin(a)
                head_points.InsertNextPoint(hx, hy, 0)

            for s in range(n_seg):
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, hpid + s)
                line.GetPointIds().SetId(1, hpid + (s + 1) % n_seg)
                head_circles.InsertNextCell(line)
                head_colors.InsertNextTuple3(cr, cg, cb)
            hpid += n_seg

        body_poly = vtk.vtkPolyData()
        body_poly.SetPoints(all_points)
        body_poly.SetLines(all_lines)
        body_poly.GetCellData().SetScalars(colors)

        body_mapper = vtk.vtkPolyDataMapper()
        body_mapper.SetInputData(body_poly)
        body_mapper.SetScalarModeToUseCellData()

        body_actor = vtk.vtkActor()
        body_actor.SetMapper(body_mapper)
        body_actor.GetProperty().SetLineWidth(2)

        head_poly = vtk.vtkPolyData()
        head_poly.SetPoints(head_points)
        head_poly.SetLines(head_circles)
        head_poly.GetCellData().SetScalars(head_colors)

        head_mapper = vtk.vtkPolyDataMapper()
        head_mapper.SetInputData(head_poly)
        head_mapper.SetScalarModeToUseCellData()

        head_actor = vtk.vtkActor()
        head_actor.SetMapper(head_mapper)
        head_actor.GetProperty().SetLineWidth(2)

        assembly = vtk.vtkAssembly()
        assembly.AddPart(body_actor)
        assembly.AddPart(head_actor)

        return assembly

    def _load_vtk_colored(self, filepath):
        """VTK 파일 로드 → 3D 졸라맨 stick figure, velocity 방향으로 회전, 걷는 모션"""
        import struct
        import math
        import re
        import vtk

        if not Path(filepath).exists():
            return None

        step_match = re.search(r'_(\d+)\.vtk$', filepath)
        step_num = int(step_match.group(1)) if step_match else 0

        with open(filepath, 'rb') as f:
            for _ in range(4):
                f.readline()
            points_line = f.readline().decode('ascii').strip()
            num_points = int(points_line.split()[1])
            points_data = f.read(num_points * 3 * 4)
            rest_bytes = f.read()

        if num_points == 0:
            return None

        vals = struct.unpack(f'>{num_points * 3}f', points_data)
        positions = [(vals[i * 3], vals[i * 3 + 1]) for i in range(num_points)]

        # --- 밀집도 계산 (spatial hash 기반) ---
        DENSITY_RADIUS = 3.0
        cell_size = DENSITY_RADIUS
        grid_map = {}
        valid = [False] * num_points
        for i in range(num_points):
            px, py = positions[i]
            if not (math.isfinite(px) and math.isfinite(py)):
                continue
            valid[i] = True
            cx = int(math.floor(px / cell_size))
            cy = int(math.floor(py / cell_size))
            grid_map.setdefault((cx, cy), []).append(i)

        densities = [0.0] * num_points
        r_sq = DENSITY_RADIUS * DENSITY_RADIUS
        for i in range(num_points):
            if not valid[i]:
                continue
            px_i, py_i = positions[i]
            cx = int(math.floor(px_i / cell_size))
            cy = int(math.floor(py_i / cell_size))
            count = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for j in grid_map.get((cx + dx, cy + dy), []):
                        if j == i:
                            continue
                        ddx = positions[j][0] - px_i
                        ddy = positions[j][1] - py_i
                        if ddx * ddx + ddy * ddy <= r_sq:
                            count += 1
            densities[i] = float(count)

        max_density = max(densities) if densities else 1.0
        if max_density < 1.0:
            max_density = 1.0

        velocities = [(0.0, 0.0)] * num_points
        try:
            header_text = rest_bytes.decode('ascii', errors='replace')
            field_offset = header_text.index('FIELD FieldData')
            cursor = header_text.index('\n', field_offset) + 1
            type_sizes = {'unsigned_char': 1, 'float': 4, 'int': 4}

            for _ in range(14):
                nl = header_text.index('\n', cursor)
                field_line = header_text[cursor:nl].strip()
                cursor = nl + 1
                parts = field_line.split()
                if len(parts) < 4:
                    continue
                fname, ncomp, ntuples, dtype = parts[0], int(parts[1]), int(parts[2]), parts[3]
                data_size = ncomp * ntuples * type_sizes.get(dtype, 4)

                if fname == 'velocity' and ncomp >= 2:
                    vel_bytes = rest_bytes[cursor:cursor + data_size]
                    vel_vals = struct.unpack(f'>{ncomp * ntuples}f', vel_bytes)
                    velocities = [(vel_vals[i * ncomp], vel_vals[i * ncomp + 1]) for i in range(ntuples)]

                cursor += data_size
                while cursor < len(header_text) and header_text[cursor] == '\n':
                    cursor += 1
        except Exception:
            pass

        H = 2.0
        TUBE_R = 0.06
        HEAD_R = 0.18

        line_points = vtk.vtkPoints()
        line_cells = vtk.vtkCellArray()
        line_scalars = vtk.vtkFloatArray()
        line_scalars.SetName('density')

        head_points = vtk.vtkPoints()
        head_scalars = vtk.vtkFloatArray()
        head_scalars.SetName('density')

        shadow_points = vtk.vtkPoints()
        shadow_cells = vtk.vtkCellArray()

        pid = 0

        for i in range(num_points):
            px, py = positions[i]
            if not valid[i]:
                continue
            vx, vy = velocities[i]
            speed = math.sqrt(vx * vx + vy * vy)

            if speed > 0.01:
                angle = math.atan2(vy, vx) - math.pi / 2
            else:
                angle = 0.0

            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            def w(lx, ly, lz):
                """로컬→월드: XY를 angle만큼 회전, Z는 높이"""
                wx = lx * cos_a - ly * sin_a + px
                wy = lx * sin_a + ly * cos_a + py
                return (wx, wy, lz)

            phase = step_num * 0.5 + i * 1.7
            swing = math.sin(phase) * 0.35
            arm_swing = -swing

            feet_z = 0.0
            hip_z = H * 0.45
            neck_z = H * 0.78
            head_z = H * 0.90

            hip = w(0, 0, hip_z)
            neck = w(0, 0, neck_z)

            l_foot = w(-H * 0.1, swing * H * 0.25, feet_z)
            r_foot = w(H * 0.1, -swing * H * 0.25, feet_z)
            l_knee = w(-H * 0.08, swing * H * 0.1, hip_z * 0.5)
            r_knee = w(H * 0.08, -swing * H * 0.1, hip_z * 0.5)

            l_shoulder = w(-H * 0.15, 0, neck_z)
            r_shoulder = w(H * 0.15, 0, neck_z)
            l_hand = w(-H * 0.18, arm_swing * H * 0.25, H * 0.50)
            r_hand = w(H * 0.18, -arm_swing * H * 0.25, H * 0.50)

            head_center = w(0, 0, head_z)

            density_val = densities[i]

            def add_seg(p1, p2):
                nonlocal pid
                id1 = line_points.InsertNextPoint(*p1)
                id2 = line_points.InsertNextPoint(*p2)
                seg = vtk.vtkLine()
                seg.GetPointIds().SetId(0, id1)
                seg.GetPointIds().SetId(1, id2)
                line_cells.InsertNextCell(seg)
                line_scalars.InsertNextValue(density_val)
                line_scalars.InsertNextValue(density_val)
                pid += 2

            add_seg(hip, neck)
            add_seg(l_shoulder, r_shoulder)
            add_seg(hip, l_knee)
            add_seg(l_knee, l_foot)
            add_seg(hip, r_knee)
            add_seg(r_knee, r_foot)
            add_seg(l_shoulder, l_hand)
            add_seg(r_shoulder, r_hand)

            head_points.InsertNextPoint(*head_center)
            head_scalars.InsertNextValue(density_val)

            shadow_pts = [hip, neck, l_shoulder, r_shoulder,
                          l_knee, r_knee, l_foot, r_foot, l_hand, r_hand]
            shadow_flat = [(p[0], p[1], 0.001) for p in shadow_pts]
            shadow_segs = [(0,1), (2,3), (0,4), (4,6), (0,5), (5,7), (2,8), (3,9)]
            for s1, s2 in shadow_segs:
                id1 = shadow_points.InsertNextPoint(*shadow_flat[s1])
                id2 = shadow_points.InsertNextPoint(*shadow_flat[s2])
                seg = vtk.vtkLine()
                seg.GetPointIds().SetId(0, id1)
                seg.GetPointIds().SetId(1, id2)
                shadow_cells.InsertNextCell(seg)

        # 밀집도 색상: 녹색(저) → 파랑 → 노랑 → 주황 → 빨강(고)
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(256)
        lut.SetRange(0.0, max_density)
        lut.SetIndexedLookup(False)
        # 커스텀 색상 그라데이션 빌드
        color_stops = [
            (0.00, (0, 255, 0)),    # 녹색 (밀집도 최저)
            (0.25, (0, 0, 255)),    # 파랑
            (0.50, (255, 255, 0)),  # 노랑
            (0.75, (255, 165, 0)),  # 주황
            (1.00, (255, 0, 0)),    # 빨강 (밀집도 최고)
        ]
        for idx in range(256):
            t = idx / 255.0
            # 구간 찾기
            for k in range(len(color_stops) - 1):
                t0, c0 = color_stops[k]
                t1, c1 = color_stops[k + 1]
                if t0 <= t <= t1:
                    f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
                    r = (c0[0] + (c1[0] - c0[0]) * f) / 255.0
                    g = (c0[1] + (c1[1] - c0[1]) * f) / 255.0
                    b = (c0[2] + (c1[2] - c0[2]) * f) / 255.0
                    lut.SetTableValue(idx, r, g, b, 1.0)
                    break
        lut.Build()

        line_poly = vtk.vtkPolyData()
        line_poly.SetPoints(line_points)
        line_poly.SetLines(line_cells)
        line_poly.GetPointData().SetScalars(line_scalars)

        tube = vtk.vtkTubeFilter()
        tube.SetInputData(line_poly)
        tube.SetRadius(TUBE_R)
        tube.SetNumberOfSides(6)
        tube.CappingOn()
        tube.Update()

        body_mapper = vtk.vtkPolyDataMapper()
        body_mapper.SetInputConnection(tube.GetOutputPort())
        body_mapper.SetScalarModeToUsePointData()
        body_mapper.SetLookupTable(lut)
        body_mapper.SetScalarRange(0.0, max_density)

        body_actor = vtk.vtkActor()
        body_actor.SetMapper(body_mapper)

        head_poly = vtk.vtkPolyData()
        head_poly.SetPoints(head_points)
        head_poly.GetPointData().SetScalars(head_scalars)

        sphere_src = vtk.vtkSphereSource()
        sphere_src.SetRadius(HEAD_R)
        sphere_src.SetPhiResolution(10)
        sphere_src.SetThetaResolution(10)

        glyph = vtk.vtkGlyph3D()
        glyph.SetInputData(head_poly)
        glyph.SetSourceConnection(sphere_src.GetOutputPort())
        glyph.SetScaleModeToDataScalingOff()
        glyph.Update()

        head_mapper = vtk.vtkPolyDataMapper()
        head_mapper.SetInputConnection(glyph.GetOutputPort())
        head_mapper.SetScalarModeToUsePointData()
        head_mapper.SetLookupTable(lut)
        head_mapper.SetScalarRange(0.0, max_density)

        head_actor = vtk.vtkActor()
        head_actor.SetMapper(head_mapper)

        shadow_poly = vtk.vtkPolyData()
        shadow_poly.SetPoints(shadow_points)
        shadow_poly.SetLines(shadow_cells)

        shadow_tube = vtk.vtkTubeFilter()
        shadow_tube.SetInputData(shadow_poly)
        shadow_tube.SetRadius(TUBE_R * 1.5)
        shadow_tube.SetNumberOfSides(4)
        shadow_tube.CappingOn()
        shadow_tube.Update()

        shadow_mapper = vtk.vtkPolyDataMapper()
        shadow_mapper.SetInputConnection(shadow_tube.GetOutputPort())
        shadow_mapper.ScalarVisibilityOff()

        shadow_actor = vtk.vtkActor()
        shadow_actor.SetMapper(shadow_mapper)
        shadow_actor.GetProperty().SetColor(0, 0, 0)
        shadow_actor.GetProperty().SetOpacity(0.3)

        assembly = vtk.vtkAssembly()
        assembly.AddPart(shadow_actor)
        assembly.AddPart(body_actor)
        assembly.AddPart(head_actor)

        return assembly

    def _anim_reload(self):
        """결과 파일 다시 스캔"""
        self._anim_stop_play()
        self._scan_vtk_results()
        self._ui.statusbar.showMessage('결과 파일을 다시 읽었습니다.')
        self._anim_preload()

    def _anim_preload(self):
        """백그라운드에서 전체 프레임 캐시에 프리로드"""
        if not self._anim_steps:
            return
        # 이미 프리로드 중이면 중단
        if hasattr(self, '_preload_timer') and self._preload_timer is not None:
            self._preload_timer.stop()

        self._preload_idx = 0
        self._preload_total = len(self._anim_steps)
        # 이미 캐시된 프레임 건너뛰기 위한 목록
        self._preload_queue = [i for i, s in enumerate(self._anim_steps) if s not in self._anim_cache]
        if not self._preload_queue:
            self._ui.statusbar.showMessage(f'전체 {self._preload_total} 프레임 캐시 완료')
            return

        self._ui.statusbar.showMessage(f'프레임 프리로드 중... 0 / {len(self._preload_queue)}')
        self._preload_timer = QTimer()
        self._preload_timer.timeout.connect(self._preload_tick)
        self._preload_timer.start(0)  # 가능한 빠르게, 하지만 UI 블로킹 없이

    def _preload_tick(self):
        """한 프레임씩 캐시에 로드"""
        if not self._preload_queue:
            self._preload_timer.stop()
            self._preload_timer = None
            self._ui.statusbar.showMessage(f'전체 {self._preload_total} 프레임 프리로드 완료')
            return

        idx = self._preload_queue.pop(0)
        step = self._anim_steps[idx]
        if step not in self._anim_cache:
            files = self._anim_files.get(step, {})
            actors = {}
            for grid_num, filepath in files.items():
                actor = self._load_vtk_colored(filepath)
                if actor:
                    actors[grid_num] = actor
            self._anim_cache[step] = actors

        loaded = self._preload_total - len(self._preload_queue)
        self._ui.statusbar.showMessage(f'프레임 프리로드 중... {loaded} / {self._preload_total}')

    def _anim_show_step(self, slider_index):
        """주어진 슬라이더 인덱스의 step을 VTK에 표시"""
        if not self._anim_steps or slider_index < 0 or slider_index >= len(self._anim_steps):
            return

        step = self._anim_steps[slider_index]
        files = self._anim_files.get(step, {})

        # 캐시에서 actor 가져오거나 새로 로드
        if step in self._anim_cache:
            new_actors = self._anim_cache[step]
        else:
            new_actors = {}
            for grid_num, filepath in files.items():
                actor = self._load_vtk_colored(filepath)
                if actor:
                    new_actors[grid_num] = actor

            # 파일을 하나도 로드하지 못한 경우 재생 중지
            if files and not new_actors:
                self._anim_stop_play()
                self._ui.statusbar.showMessage('결과 파일을 찾을 수 없습니다. 경로를 확인해주세요.')
                return

            self._anim_cache[step] = new_actors

        cam = self.vtk.renderer.GetActiveCamera()
        cam_pos = cam.GetPosition()
        cam_focal = cam.GetFocalPoint()
        cam_up = cam.GetViewUp()
        cam_scale = cam.GetParallelScale()

        render_window = self.vtk.vtk_widget.GetRenderWindow()
        render_window.SetSwapBuffers(False)

        all_grids = set()
        for s in self._anim_files.values():
            all_grids.update(s.keys())
        for grid_num in all_grids:
            self.vtk.obj_manager.group(f'grid{grid_num}').remove()

        from nextlib.vtk.core.object_manager import ObjectData
        for grid_num, actor in new_actors.items():
            self.vtk.renderer.AddActor(actor)
            obj_id = self.vtk.obj_manager._next_id
            self.vtk.obj_manager._next_id += 1
            try:
                r, g, b = actor.GetProperty().GetColor()
                color = (int(r*255), int(g*255), int(b*255))
            except AttributeError:
                color = (255, 255, 255)
            obj = ObjectData(
                id=obj_id, actor=actor, name=f'grid{grid_num}_{step}',
                group=f'grid{grid_num}', color=color)
            self.vtk.obj_manager._objects[obj_id] = obj

        cam.SetPosition(cam_pos)
        cam.SetFocalPoint(cam_focal)
        cam.SetViewUp(cam_up)
        cam.SetParallelScale(cam_scale)
        self.vtk.renderer.ResetCameraClippingRange()

        render_window.SetSwapBuffers(True)
        render_window.Render()

        self._anim_spin.blockSignals(True)
        self._anim_spin.setMaximum(len(self._anim_steps))
        self._anim_spin.setValue(slider_index + 1)
        self._anim_spin.blockSignals(False)
        self._anim_total_label.setText(f'/ {len(self._anim_steps)}')

    def _anim_slider_changed(self, value):
        self._anim_show_step(value)

    def _anim_spin_changed(self, value):
        """스핀박스에서 프레임 번호 직접 입력 시"""
        self._anim_slider.setValue(value - 1)

    def _anim_first(self):
        self._anim_stop_play()
        self._anim_slider.setValue(0)

    def _anim_prev(self):
        self._anim_stop_play()
        v = self._anim_slider.value()
        if v > 0:
            self._anim_slider.setValue(v - 1)

    def _anim_next(self):
        self._anim_stop_play()
        v = self._anim_slider.value()
        if v < self._anim_slider.maximum():
            self._anim_slider.setValue(v + 1)

    def _anim_last(self):
        self._anim_stop_play()
        self._anim_slider.setValue(self._anim_slider.maximum())

    def _anim_play_pause(self):
        if self._anim_playing:
            self._anim_stop_play()
        else:
            self._anim_playing = True
            self._btn_anim_play.setIcon(self._icon_stop)
            self._anim_timer.start(self._anim_speed_ms)

    def _anim_speed_changed(self, index):
        speeds = {0: 200, 1: 133, 2: 100, 3: 50, 4: 25, 5: 12, 6: 6, 7: 3}  # x1~x64
        self._anim_speed_ms = speeds.get(index, 200)
        if self._anim_playing:
            self._anim_timer.start(self._anim_speed_ms)

    def _anim_stop_play(self):
        self._anim_playing = False
        self._anim_timer.stop()
        self._btn_anim_play.setIcon(self._icon_play)

    def _anim_tick(self):
        v = self._anim_slider.value()
        if v < self._anim_slider.maximum():
            self._anim_slider.setValue(v + 1)
        else:
            self._anim_slider.setValue(0)

    def _anim_export_video(self):
        """애니메이션을 동영상 파일(MP4)로 저장 - 설정 다이얼로그 표시"""
        if not self._anim_steps:
            return

        self._anim_stop_play()

        # 이미 열려있으면 포커스만
        if hasattr(self, '_export_dlg') and self._export_dlg is not None:
            self._export_dlg.raise_()
            self._export_dlg.activateWindow()
            return

        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                        QRadioButton, QGroupBox, QLabel,
                                        QSpinBox, QPushButton)

        total = len(self._anim_steps)

        dlg = QDialog(self)
        dlg.setWindowTitle('동영상 내보내기')
        dlg.setFixedWidth(350)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        layout = QVBoxLayout(dlg)

        # 프레임 범위 선택
        range_box = QGroupBox(f'프레임 범위 (전체: 1 ~ {total})')
        range_grid = QVBoxLayout(range_box)

        # 시작 프레임
        start_row = QHBoxLayout()
        start_row.addWidget(QLabel('시작:'))
        spin_start = QSpinBox()
        spin_start.setMinimum(1)
        spin_start.setMaximum(total)
        spin_start.setValue(1)
        spin_start.setFixedWidth(70)
        start_row.addWidget(spin_start)
        btn_set_start = QPushButton('현재 프레임')
        btn_set_start.setFixedWidth(100)
        btn_set_start.clicked.connect(lambda: spin_start.setValue(self._anim_slider.value() + 1))
        start_row.addWidget(btn_set_start)
        range_grid.addLayout(start_row)

        # 끝 프레임
        end_row = QHBoxLayout()
        end_row.addWidget(QLabel('끝:    '))
        spin_end = QSpinBox()
        spin_end.setMinimum(1)
        spin_end.setMaximum(total)
        spin_end.setValue(total)
        spin_end.setFixedWidth(70)
        end_row.addWidget(spin_end)
        btn_set_end = QPushButton('현재 프레임')
        btn_set_end.setFixedWidth(100)
        btn_set_end.clicked.connect(lambda: spin_end.setValue(self._anim_slider.value() + 1))
        end_row.addWidget(btn_set_end)
        range_grid.addLayout(end_row)

        layout.addWidget(range_box)

        # 시작 > 끝 방지
        spin_start.valueChanged.connect(lambda v: spin_end.setValue(max(v, spin_end.value())))
        spin_end.valueChanged.connect(lambda v: spin_start.setValue(min(v, spin_start.value())))

        # 화질 선택
        group_box = QGroupBox('화질 선택')
        group_layout = QVBoxLayout(group_box)
        btn_mid = QRadioButton('중간 품질 (1x)')
        btn_good = QRadioButton('높은 품질 (1.5x)')
        btn_high = QRadioButton('원본급 (2x)')
        btn_good.setChecked(True)
        group_layout.addWidget(btn_mid)
        group_layout.addWidget(btn_good)
        group_layout.addWidget(btn_high)
        layout.addWidget(group_box)

        # 버튼
        btn_row = QHBoxLayout()
        btn_export = QPushButton('내보내기')
        btn_export.setDefault(True)
        btn_cancel = QPushButton('취소')
        btn_row.addStretch()
        btn_row.addWidget(btn_export)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        btn_cancel.clicked.connect(dlg.close)

        def do_export():
            frame_start = spin_start.value() - 1
            frame_end = spin_end.value()
            if btn_high.isChecked():
                scale_factor = 2
            elif btn_good.isChecked():
                scale_factor = 1.5
            else:
                scale_factor = 1
            dlg.close()
            self._do_anim_export(frame_start, frame_end, scale_factor)

        btn_export.clicked.connect(do_export)

        self._export_dlg = dlg
        dlg.destroyed.connect(lambda: setattr(self, '_export_dlg', None))
        dlg.show()

    def _do_anim_export(self, frame_start, frame_end, scale_factor):
        """실제 동영상 내보내기 실행"""
        from PySide6.QtWidgets import QFileDialog, QProgressDialog, QApplication

        default_path = str(Path(self.prj.path) / f'{self.prj.name}_animation.mp4')
        filepath, _ = QFileDialog.getSaveFileName(
            self, '동영상 저장', default_path,
            'MP4 Video (*.mp4);;AVI Video (*.avi)')
        if not filepath:
            return

        import vtk

        render_window = self.vtk.vtk_widget.GetRenderWindow()
        orig_size = render_window.GetSize()

        interactor = self.vtk.vtk_widget.GetRenderWindow().GetInteractor()
        interactor.Disable()
        self.vtk.vtk_widget.setEnabled(False)
        self._anim_bar.setEnabled(False)

        # 카메라 상태를 리사이즈 전에 저장
        cam = self.vtk.renderer.GetActiveCamera()
        cam_pos = cam.GetPosition()
        cam_focal = cam.GetFocalPoint()
        cam_up = cam.GetViewUp()
        cam_scale = cam.GetParallelScale()

        # 오프스크린으로 전환하여 화면 깜빡임 방지
        render_window.SetOffScreenRendering(True)

        if scale_factor > 1:
            render_window.SetSize(int(orig_size[0] * scale_factor), int(orig_size[1] * scale_factor))

        # 카메라 복원 함수
        def _restore_cam():
            cam.SetPosition(cam_pos)
            cam.SetFocalPoint(cam_focal)
            cam.SetViewUp(cam_up)
            cam.SetParallelScale(cam_scale)
            self.vtk.renderer.ResetCameraClippingRange()

        _restore_cam()
        render_window.Render()

        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(render_window)
        w2i.SetInputBufferTypeToRGB()
        w2i.ReadFrontBufferOff()

        export_count = frame_end - frame_start

        progress = QProgressDialog(f'동영상 저장 중... (프레임 {frame_start+1}~{frame_end})', '취소', 0, export_count, self)
        progress.setWindowTitle('동영상 내보내기')
        progress.setMinimumDuration(0)
        progress.setValue(0)

        try:
            import cv2
            import numpy as np
            from vtk.util.numpy_support import vtk_to_numpy

            self._anim_show_step(frame_start)
            _restore_cam()
            render_window.Render()
            w2i.Modified()
            w2i.Update()
            img_data = w2i.GetOutput()
            dims = img_data.GetDimensions()
            width, height = dims[0], dims[1]

            ext = Path(filepath).suffix.lower()
            if ext == '.avi':
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            fps = 5
            writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

            for i in range(frame_start, frame_end):
                if progress.wasCanceled():
                    break

                self._anim_show_step(i)
                _restore_cam()
                render_window.Render()

                w2i.Modified()
                w2i.Update()
                img_data = w2i.GetOutput()

                vtk_array = img_data.GetPointData().GetScalars()
                np_arr = vtk_to_numpy(vtk_array)
                np_arr = np_arr.reshape(height, width, 3)
                np_arr = np.flip(np_arr, axis=0)
                bgr = cv2.cvtColor(np_arr, cv2.COLOR_RGB2BGR)
                writer.write(bgr)

                progress.setValue(i - frame_start + 1)
                QApplication.processEvents()

            writer.release()

        except ImportError:
            progress.close()
            try:
                ogv_writer = vtk.vtkOggTheoraWriter()
                ogv_writer.SetFileName(filepath.replace('.mp4', '.ogv').replace('.avi', '.ogv'))
                ogv_writer.SetInputConnection(w2i.GetOutputPort())
                ogv_writer.SetRate(5)
                ogv_writer.Start()

                for i in range(frame_start, frame_end):
                    self._anim_show_step(i)
                    _restore_cam()
                    render_window.Render()
                    w2i.Modified()
                    w2i.Update()
                    ogv_writer.Write()

                ogv_writer.End()
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, '오류', f'동영상 저장 실패: {e}\ncv2(opencv-python) 설치를 권장합니다.')
                render_window.SetOffScreenRendering(False)
                if scale_factor > 1:
                    render_window.SetSize(orig_size[0], orig_size[1])
                _restore_cam()
                render_window.Render()
                interactor.Enable()
                self.vtk.vtk_widget.setEnabled(True)
                self._anim_bar.setEnabled(True)
                return

        # 오프스크린 해제 및 원래 상태 복원
        render_window.SetOffScreenRendering(False)
        if scale_factor > 1:
            render_window.SetSize(orig_size[0], orig_size[1])

        _restore_cam()
        render_window.Render()

        interactor.Enable()
        self.vtk.vtk_widget.setEnabled(True)
        self._anim_bar.setEnabled(True)

        progress.close()

        quality_labels = {2: '원본급', 1.5: '높은 품질', 1: '중간 품질'}
        quality_label = quality_labels.get(scale_factor, f'{scale_factor}x')
        self._ui.statusbar.showMessage(f'동영상 저장 완료 ({quality_label}, {width}x{height}): {filepath}')
