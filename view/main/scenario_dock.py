"""오른쪽 Properties 독 위에 배치되는 "Scenario" 독 위젯

< Common > : 미리 준비된 시나리오 프리셋(datarw/e8ight/presets/*.json) 5개 버튼
< Custom > : 사용자가 이름을 지어 현재 설정을 저장/재적용할 수 있는 5개 슬롯

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.app_info, self.prj, self._ui, self.load_input_file(), self.save_input_file(),
self._load_background_map()
"""
import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                               QGroupBox, QPushButton, QInputDialog, QMessageBox,
                               QSizePolicy, QMenu)

from datarw.e8ight.solver_input import SolverData

_PRESET_NAMES = ['S1_simple_exit', 'S2_corridor_obstacle', 'S3_crowd_surge',
                 'S4_entry', 'S5_counterflow']
_CUSTOM_SLOT_COUNT = 5

# Properties 패널의 그룹박스(예: materials_view.py)와 동일한 스타일
_GROUPBOX_STYLE = (
    "QGroupBox {"
    "    border: 1px solid;"
    "    border-radius: 6;"
    "    margin-top: 9;"
    "    border-color : #c8c8c8;"
    "    padding: 3;   "
    "}"
    "QGroupBox::title {"
    "    subcontrol-origin: margin;"
    "    subcontrol-position: top left;"
    "    left: 10;"
    "    padding: 2 3;"
    "}")


def _make_groupbox(title):
    box = QGroupBox(title)
    box.setSizePolicy(box.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)
    font = QFont()
    font.setPointSize(8)
    font.setBold(True)
    box.setFont(font)
    box.setStyleSheet(_GROUPBOX_STYLE)
    return box


class ScenarioDockMixin:
    """Scenario 독 위젯: Common 프리셋 적용 + Custom 슬롯 저장/적용"""

    def _init_scenario_dock(self):
        self._custom_scenarios = self._load_custom_scenarios_state()

        dock = QDockWidget('Scenario', self)
        dock.setObjectName('dockWidget_scenario')
        # 다른 독(Properties 등)과 동일한 타이틀바 폰트로 맞춘다
        dock_font = QFont()
        dock_font.setPointSize(10)
        dock_font.setBold(True)
        dock.setFont(dock_font)

        content = QWidget()
        layout = QVBoxLayout(content)

        group_common = _make_groupbox('< Common >')
        common_layout = QHBoxLayout(group_common)
        common_layout.setContentsMargins(8, 12, 8, 4)
        self._common_scenario_buttons = []
        for name in _PRESET_NAMES:
            btn = QPushButton()
            btn.clicked.connect(lambda checked=False, n=name: self._show_common_menu(n))
            common_layout.addWidget(btn)
            self._common_scenario_buttons.append((name, btn))
        layout.addWidget(group_common)

        group_custom = _make_groupbox('< Custom >')
        custom_layout = QHBoxLayout(group_custom)
        custom_layout.setContentsMargins(8, 12, 8, 4)
        self._custom_scenario_buttons = []
        for idx in range(_CUSTOM_SLOT_COUNT):
            btn = QPushButton()
            btn.clicked.connect(lambda checked=False, i=idx: self._show_custom_menu(i))
            custom_layout.addWidget(btn)
            self._custom_scenario_buttons.append(btn)
        layout.addWidget(group_custom)

        content.setSizePolicy(content.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)

        self._refresh_common_scenario_buttons()
        self._refresh_custom_scenario_buttons()

        dock.setWidget(content)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self.splitDockWidget(dock, self._ui.dockWidget_properties, Qt.Orientation.Vertical)
        self._ui.dockWidget_scenario = dock

        # QMainWindow는 splitter 안 두 dock의 남는 세로 공간을 균등 배분하려 하므로,
        # Scenario 쪽은 내용물 높이로, 나머지는 Properties가 받도록 명시적으로 고정한다.
        content.adjustSize()
        self.resizeDocks([dock], [content.sizeHint().height()], Qt.Orientation.Vertical)

    # ------------------------------------------------------------------
    # Common 프리셋
    # ------------------------------------------------------------------
    def _presets_dir(self):
        return self.app_info.path / 'datarw' / 'e8ight' / 'presets'

    def _common_label(self, preset_name):
        labels = self._custom_scenarios.get('common_labels', {})
        return labels.get(preset_name) or preset_name.split('_')[0]  # 'S1_simple_exit' -> 'S1'

    def _refresh_common_scenario_buttons(self):
        for preset_name, btn in self._common_scenario_buttons:
            label = self._common_label(preset_name)
            btn.setText(label)
            btn.setToolTip(f'{preset_name}\n클릭: 메뉴 열기 (프리셋 적용 / 현재값으로 저장 / 이름 변경)')

    def _show_common_menu(self, preset_name):
        btn = next(b for n, b in self._common_scenario_buttons if n == preset_name)
        menu = QMenu(self)
        menu.addAction('프리셋 적용', lambda: self._apply_common_preset(preset_name))
        menu.addAction('현재값으로 저장', lambda: self._save_current_as_common_preset(preset_name))
        menu.addAction('이름 변경', lambda: self._rename_common_preset(preset_name))
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def _rename_common_preset(self, preset_name):
        current = self._common_label(preset_name)
        new_label, ok = QInputDialog.getText(
            self, '버튼 이름 편집', '버튼에 표시할 이름을 입력하세요:', text=current)
        new_label = new_label.strip()
        if not ok or not new_label:
            return

        self._custom_scenarios.setdefault('common_labels', {})[preset_name] = new_label
        self._save_custom_scenarios_state()
        self._refresh_common_scenario_buttons()

    def _apply_common_preset(self, preset_name):
        preset_path = self._presets_dir() / f'{preset_name}.json'
        if not preset_path.is_file():
            QMessageBox.warning(self, 'Scenario', f'프리셋 파일을 찾을 수 없습니다:\n{preset_path}')
            return

        try:
            preset_data = json.loads(preset_path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as e:
            QMessageBox.warning(self, 'Scenario', f'프리셋 파일을 읽는 중 오류가 발생했습니다:\n{e}')
            return

        self._apply_scenario_data(
            preset_data,
            f'"{preset_name}" 프리셋을 적용하시겠습니까?\n프리셋에 정의된 항목만 현재 설정에 덮어써지고,\n'
            f'프리셋에 없는 항목(현재 값)은 그대로 유지됩니다.')

    def _save_current_as_common_preset(self, preset_name):
        """개발 단계에서 S1~S5 기본 프리셋 파일 자체를 현재 설정으로 갱신한다."""
        if not self.prj.path:
            QMessageBox.warning(self, 'Scenario', '먼저 프로젝트를 열거나 생성해주세요.')
            return

        reply = QMessageBox.question(
            self, 'Scenario',
            f'현재 설정으로 "{preset_name}" 프리셋 파일을 덮어쓰시겠습니까?\n'
            f'(이 프리셋을 쓰는 모든 프로젝트에 영향을 줍니다)',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.save_input_file()
        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
        if not json_path.is_file():
            QMessageBox.warning(self, 'Scenario', '현재 설정을 저장하지 못했습니다.')
            return

        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as e:
            QMessageBox.warning(self, 'Scenario', f'현재 설정을 읽는 중 오류가 발생했습니다:\n{e}')
            return

        preset_path = self._presets_dir() / f'{preset_name}.json'
        preset_path.parent.mkdir(parents=True, exist_ok=True)
        preset_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        self._ui.statusbar.showMessage(f'"{preset_name}" 프리셋을 현재 설정으로 갱신했습니다.')

    # ------------------------------------------------------------------
    # Custom 슬롯: 이름 없으면 저장, 이름 있으면 적용
    # ------------------------------------------------------------------
    def _custom_scenarios_file(self):
        return self.app_info.user_path / 'CrowdSim' / 'custom_scenarios.json'

    def _load_custom_scenarios_state(self):
        path = self._custom_scenarios_file()
        if not path.is_file():
            return {}
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            return {}

    def _save_custom_scenarios_state(self):
        path = self._custom_scenarios_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._custom_scenarios, ensure_ascii=False, indent=2), encoding='utf-8')

    def _refresh_custom_scenario_buttons(self):
        for idx, btn in enumerate(self._custom_scenario_buttons):
            slot = self._custom_scenarios.get(str(idx))
            if slot and slot.get('name'):
                btn.setText(slot['name'])
                btn.setToolTip(f"클릭: 메뉴 열기 (\"{slot['name']}\" 불러오기 / 현재값으로 저장 / 이름 변경)")
            else:
                btn.setText('+')
                btn.setToolTip('클릭: 현재 설정을 이름 붙여 저장')

    def _show_custom_menu(self, idx):
        slot = self._custom_scenarios.get(str(idx))
        if not slot or not slot.get('name'):
            # 아직 저장 안 된 빈 슬롯("+")은 바로 이름을 물어 저장한다
            self._save_current_as_custom_slot(idx)
            return

        btn = self._custom_scenario_buttons[idx]
        menu = QMenu(self)
        menu.addAction('설정 불러오기', lambda: self._apply_custom_slot(idx))
        menu.addAction('현재값으로 저장', lambda: self._save_current_as_custom_slot(idx))
        menu.addAction('이름 변경', lambda: self._rename_custom_slot(idx))
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def _rename_custom_slot(self, idx):
        slot = self._custom_scenarios.get(str(idx))
        if not slot or not slot.get('name'):
            return  # 아직 저장 안 된 빈 슬롯("+")은 편집할 이름이 없음

        new_name, ok = QInputDialog.getText(
            self, '버튼 이름 편집', '버튼에 표시할 이름을 입력하세요:', text=slot['name'])
        new_name = new_name.strip()
        if not ok or not new_name:
            return

        slot['name'] = new_name
        self._save_custom_scenarios_state()
        self._refresh_custom_scenario_buttons()

    def _apply_custom_slot(self, idx):
        slot = self._custom_scenarios.get(str(idx))
        if not slot or not slot.get('name'):
            return
        self._apply_scenario_data(
            slot['data'],
            f'"{slot["name"]}" 저장된 설정을 적용하시겠습니까?\n저장된 항목만 현재 설정에 덮어써지고,\n'
            f'저장되지 않은 항목(현재 값)은 그대로 유지됩니다.')

    def _save_current_as_custom_slot(self, idx):
        if not self.prj.path:
            QMessageBox.warning(self, 'Scenario', '먼저 프로젝트를 열거나 생성해주세요.')
            return

        slot = self._custom_scenarios.get(str(idx))
        default_name = slot['name'] if slot and slot.get('name') else ''
        name, ok = QInputDialog.getText(self, 'Custom 시나리오 저장', '저장할 이름을 입력하세요:',
                                         text=default_name)
        name = name.strip()
        if not ok or not name:
            return

        self.save_input_file()
        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
        if not json_path.is_file():
            QMessageBox.warning(self, 'Scenario', '현재 설정을 저장하지 못했습니다.')
            return

        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as e:
            QMessageBox.warning(self, 'Scenario', f'현재 설정을 읽는 중 오류가 발생했습니다:\n{e}')
            return

        self._custom_scenarios[str(idx)] = {'name': name, 'data': data}
        self._save_custom_scenarios_state()
        self._refresh_custom_scenario_buttons()

    # ------------------------------------------------------------------
    # 공통 적용 로직: config.* 항목 단위로 "있는 것만" 덮어쓰고 나머지는 보존
    # ------------------------------------------------------------------
    def _apply_scenario_data(self, preset_data, confirm_message):
        if not self.prj.path:
            QMessageBox.warning(self, 'Scenario', '먼저 프로젝트를 열거나 생성해주세요.')
            return

        reply = QMessageBox.question(
            self, 'Scenario', confirm_message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
        solver = SolverData()
        if json_path.is_file():
            solver.load(json_path)
        else:
            solver.create(str(json_path))

        preset_config = (preset_data or {}).get('config') or {}
        for key, value in preset_config.items():
            solver.data.set(f'config.{key}', value)

        solver.save()

        self.load_input_file()
        self._load_background_map()
        self._ui.statusbar.showMessage('시나리오가 적용되었습니다.')
