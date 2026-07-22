import os
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import (QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QMenu, QDialog,
                               QLabel, QPushButton, QTextBrowser, QLineEdit, QFileDialog,
                               QMessageBox, QApplication)
from PySide6.QtCore import QSize, QSettings, Qt, QPointF, QTimer
from PySide6.QtGui import (QAction, QCursor, QPixmap, QPainter, QColor, QIcon,
                           QPen, QPolygonF)

from nextlib.utils.ui import load_ui
from nextlib.utils.file import make_dir
from nextlib.dialogbox.dialogbox import DirDialogBox
from nextlib.vtk.vtk_widget_base import VtkWidgetBase
from nextlib.widgets.dropdown import DropDown
from nextlib.widgets.tree import TreeWidget
from nextlib.widgets.icon import create_icon
from nextlib.execute.exec_widget import ExecWidget

from view.main.main_window_view_ui import Ui_MainWindowView
from view.main.animation_bar import AnimationMixin
from view.main.solver_runner import SolverRunMixin
from view.main.video_export import VideoExportMixin
from view.main.background_map import BackgroundMapMixin

from view.panel.properties.solver_common_view import SolverCommonView
from view.panel.properties.grid_view import GridView
from view.panel.properties.materials_view import MaterialsView
from view.panel.properties.particle_view import ParticleView
from view.panel.properties.inlet_view import InletView
from view.panel.properties.outlet_view import OutletView
from view.panel.properties.zone_view import ZoneView
from view.panel.properties.report_view import ReportView
from view.panel.properties.export_view import ExportView

from datarw.e8ight.solver_input import SolverData


@dataclass
class ProjectInfor:
    version: int = 1.00
    path: str = ''
    name: str = 'NoNamed'


class MainWindowView(QMainWindow, AnimationMixin, SolverRunMixin,
                     VideoExportMixin, BackgroundMapMixin):
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
        self.prop_zone = ZoneView(self)
        self.prop_report = ReportView(self)
        self.prop_export = ExportView(self)

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
        _vtk_layout.addWidget(self._create_anim_bar())

        self._ui.verticalLayout_vtk.addWidget(_vtk_frame)
        self.cmd = ExecWidget(self)
        self.properties = DropDown(self._ui.verticalLayout_properties)

        self.solver_watcher = None
        self._solver_proc = None
        self._bg_map_actor = None
        self._bg_overlay_actor = None

        self._initialize()

    def _initialize(self):
        self.cmd.put_in_layout(self._ui.verticalLayout_command)
        self.cmd.connect_to_statusbar(self._ui.statusbar)

        self.tree.itemDoubleClickedWithPos.connect(lambda pos, col: self._fold_property_item(pos))
        self.tree.itemsSelectedWithPos.connect(self._changed_selection_items)

        self._init_toolbar()
        self._init_menu_connections()

        self.resize(1400, 960)
        # 마우스가 있는 모니터 중앙에 배치
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
        os.startfile(self.prj.path)

    def _open_terminal(self):
        if not self.prj.path:
            return
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

    def _make_bg_map_icon(self):
        """배경 이미지 버튼 아이콘 (산 + 태양)"""
        pix = QPixmap(32, 32)
        pix.fill(QColor(0, 0, 0, 0))
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 산 모양
        p.setPen(QPen(QColor(60, 120, 60), 2))
        p.setBrush(QColor(100, 180, 100))
        p.drawPolygon(QPolygonF([QPointF(2, 26), QPointF(12, 8), QPointF(22, 26)]))
        p.drawPolygon(QPolygonF([QPointF(14, 26), QPointF(24, 12), QPointF(30, 26)]))
        # 태양
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 200, 50))
        p.drawEllipse(22, 2, 8, 8)
        p.end()
        return QIcon(pix)

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

        self.action_bg_map = QAction(self._make_bg_map_icon(), '배경 이미지', self)
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
        self.tree.insert([6], 'Zone')
        self.tree.insert([7], 'Report')
        self.tree.insert([8], 'Export')

        for i in range(9):
            self.tree.set_editable([i], 0, editable=False)

    def _fold_property_item(self, pos):
        if not pos or len(pos) != 1:
            return

        idx = pos[0]
        if self.properties.is_item_open(idx):
            self.properties.close_item(idx)
        else:
            self.properties.open_item(idx)

    def _changed_selection_items(self, positions):
        """트리 선택 변경 시: 단일 선택이면 그 항목만 맨 위로 스크롤하고,
        다중 선택이면 스크롤 없이 선택된 항목들만(열림/닫힘 상태와 무관하게) 표시한다."""
        indices = [pos[0] for pos in positions if len(pos) == 1]
        if len(indices) == 1:
            self.properties.show_all()
            self.properties.scroll_to_item(indices[0])
        elif len(indices) > 1:
            self.properties.show_only(indices)

    def set_defaults_vtk(self):
        self._stop_preload()
        self.vtk.obj_manager.all().remove()
        self._remove_background_actors()
        self._anim_reset()
        self.vtk.vtk_widget.GetRenderWindow().Render()

    def set_defaults_properties(self):
        self.properties.set_defaults()

        self.properties.insert_item(0, '해석 일반', self.prop_solverCommon.get_widget())

        self.properties.insert_item(1, 'Grid', self.prop_grid.get_widget())
        self.properties.insert_item(2, 'Materials', self.prop_materials.get_widget())

        self.properties.insert_item(3, 'Particle', self.prop_particle.get_widget())
        self.properties.insert_item(4, 'Inlet', self.prop_inlet.get_widget())
        self.properties.insert_item(5, 'Outlet', self.prop_outlet.get_widget())
        self.properties.insert_item(6, 'Zone', self.prop_zone.get_widget())

        self.properties.insert_item(7, 'Report', self.prop_report.get_widget())
        self.properties.insert_item(8, 'Export', self.prop_export.get_widget())

    def _property_views(self):
        """입력 파일과 연동되는 설정 패널 목록 (저장/로드 순서와 동일)"""
        return (self.prop_solverCommon, self.prop_grid, self.prop_materials,
                self.prop_particle, self.prop_inlet, self.prop_outlet, self.prop_zone, self.prop_report,
                self.prop_export)

    def new_project(self, parent=None):
        dlg = QDialog(parent or self)
        dlg.setWindowTitle('새 프로젝트')
        dlg.setFixedWidth(450)
        layout = QVBoxLayout(dlg)

        # 최근 경로 불러오기 (없으면 바탕화면)
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

        for prop in self._property_views():
            prop.load_input_file(solver)

    def save_input_file(self):
        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')

        solver = SolverData()
        if json_path.is_file():
            solver.load(json_path)
        else:
            solver.create(json_path)

        # 각 패널이 자체적으로 전체 목록을 재구성하는 항목은 append 중복을 막기 위해 비워둔다.
        # (result_report처럼 dict.update로 병합되는 항목이나, GUI가 다루지 않는 필드는 그대로 보존됨)
        for key in ('grid', 'materials', 'particle_generation', 'inlet', 'outlet', 'zone'):
            solver.data.set(f'config.{key}', [])

        for prop in self._property_views():
            solver = prop.save_input_file(solver)

        solver.save()

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
