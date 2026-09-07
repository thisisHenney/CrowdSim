from nextlib.utils.ui import load_ui
from view.panel.properties.zone_ui import Ui_ZoneForm
from view.panel.properties import _extra_ui


_KNOWN_ZONE_KEYS = {'_comment', 'p1', 'p2', 'direction', 'length', 'zone_type',
                    'K_avo', 'avoid_radius', 'outlet_id', 'grid'}


_EDIT_FIELDS = (
    'lineEdit_p1_x',
    'lineEdit_p1_y',
    'lineEdit_p2_x',
    'lineEdit_p2_y',
    'lineEdit_direction_x',
    'lineEdit_direction_y',
    'lineEdit_length',
    'comboBox_zone_type',
    'lineEdit_k_avo',
    'lineEdit_avoid_radius',
    'lineEdit_outlet_id',
    'lineEdit_grid',
    # 항목이 없으면 저장/삭제도 대상이 없다.
    # ('추가'는 잠그지 않는다 - 첫 항목을 만드는 유일한 길이다)
    'pushButton_save',
    'pushButton_remove',
)


class ZoneData:
    def __init__(self):
        self.comment = ''
        self.p1 = [0, 0]
        self.p2 = [0, 0]
        self.direction = [0, 1]
        self.length = 1.0
        self.zone_type = 'avoid_zone'
        self.k_avo = 200.0
        self.avoid_radius = 15.0
        self.outlet_id = 0
        self.grid = 1
        self.raw_extra = {}


class ZoneView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.ui = load_ui(None, Ui_ZoneForm).ui

        self.zone_data = []
        self._initialize()

    def _initialize(self):
        ui = self.ui

        ui.comboBox_name.currentIndexChanged.connect(self._changed_combo_name)
        ui.pushButton_add.clicked.connect(self._clicked_add)
        ui.pushButton_save.clicked.connect(self._clicked_save)
        ui.pushButton_remove.clicked.connect(self._clicked_remove)

        # 목록이 비어 있는 초기 상태에서는 입력란을 잠가 둔다.
        # ('추가'를 눌러 항목이 생기면 change_data()가 다시 켠다)
        _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)

        # 항목별 "저장" 버튼을 누르지 않아도 입력값이 메모리에 남게 한다.
        # (파일에는 툴바 Save/Run 때만 기록된다)
        _extra_ui.connect_autosave(ui, _EDIT_FIELDS, self._autosave_current)

    def _changed_combo_name(self, index):
        if index == -1:
            return
        self.change_data(index)

    def _autosave_current(self, *args):
        """입력란이 편집될 때마다 현재 항목에 즉시 반영한다.

        _filling 중에는 무시한다 - change_data()가 위젯을 채우는 동안에도
        시그널이 오는데, 그대로 두면 새로 채운 값이 이전 항목에 덮어써진다.
        """
        if getattr(self, '_filling', False):
            return
        ui = self.ui
        index = ui.comboBox_name.currentIndex()
        if not (0 <= index < len(self.zone_data)):
            return
        self.get_cur_data(self.zone_data[index])
        parent = getattr(self, '_parent', None)
        if parent is not None and hasattr(parent, 'set_dirty'):
            parent.set_dirty(True)

    def change_data(self, index):
        self._filling = True
        try:
            ui = self.ui
            index = index if self.zone_data and (0 <= index < len(self.zone_data)) else (
                len(self.zone_data) - 1 if len(self.zone_data) > 0 else -1)

            if index == -1:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)
                ui.lineEdit_p1_x.setText('0')
                ui.lineEdit_p1_y.setText('0')
                ui.lineEdit_p2_x.setText('0')
                ui.lineEdit_p2_y.setText('0')
                ui.lineEdit_direction_x.setText('0')
                ui.lineEdit_direction_y.setText('1')
                ui.lineEdit_length.setText('1.0')
                ui.comboBox_zone_type.setCurrentText('avoid_zone')
                ui.lineEdit_k_avo.setText('200.0')
                ui.lineEdit_avoid_radius.setText('15.0')
                ui.lineEdit_outlet_id.setText('0')
                ui.lineEdit_grid.setText('1')

            else:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, True)
                cur_data = self.zone_data[index]

                ui.lineEdit_p1_x.setText(str(cur_data.p1[0]))
                ui.lineEdit_p1_y.setText(str(cur_data.p1[1]))
                ui.lineEdit_p2_x.setText(str(cur_data.p2[0]))
                ui.lineEdit_p2_y.setText(str(cur_data.p2[1]))
                ui.lineEdit_direction_x.setText(str(cur_data.direction[0]))
                ui.lineEdit_direction_y.setText(str(cur_data.direction[1]))
                ui.lineEdit_length.setText(str(cur_data.length))
                ui.comboBox_zone_type.setCurrentText(cur_data.zone_type)
                ui.lineEdit_k_avo.setText(str(cur_data.k_avo))
                ui.lineEdit_avoid_radius.setText(str(cur_data.avoid_radius))
                ui.lineEdit_outlet_id.setText(str(cur_data.outlet_id))
                ui.lineEdit_grid.setText(str(cur_data.grid))
        finally:
            self._filling = False

    def _clicked_add(self):
        self.add_data()
        _extra_ui.mark_dirty(self)

    def _clicked_save(self):
        self.save_data()
        _extra_ui.mark_dirty(self)

    def _clicked_remove(self):
        self.remove_data()
        _extra_ui.mark_dirty(self)

    def get_widget(self):
        return self.ui.widget

    def add_data(self):
        ui = self.ui

        get_data = self.get_cur_data(ZoneData())

        self.zone_data.append(get_data)
        ui.comboBox_name.addItem(get_data.comment or f'zone_{len(self.zone_data) - 1}')
        ui.comboBox_name.setCurrentIndex(len(self.zone_data) - 1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.comment = ui.comboBox_name.currentText()

        get_data.p1[0] = ui.lineEdit_p1_x.text()
        get_data.p1[1] = ui.lineEdit_p1_y.text()
        get_data.p2[0] = ui.lineEdit_p2_x.text()
        get_data.p2[1] = ui.lineEdit_p2_y.text()
        get_data.direction[0] = ui.lineEdit_direction_x.text()
        get_data.direction[1] = ui.lineEdit_direction_y.text()

        get_data.length = ui.lineEdit_length.text()
        get_data.zone_type = ui.comboBox_zone_type.currentText()
        get_data.k_avo = ui.lineEdit_k_avo.text()
        get_data.avoid_radius = ui.lineEdit_avoid_radius.text()
        get_data.outlet_id = ui.lineEdit_outlet_id.text()
        get_data.grid = ui.lineEdit_grid.text()

        return get_data

    def save_data(self, index=-1):
        ui = self.ui

        if index == -1:
            index = ui.comboBox_name.currentIndex()

        cur_data = self.zone_data[index]
        cur_data.comment = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.comment)
        self.get_cur_data(cur_data)

    def load_input_file(self, solver):
        ui = self.ui
        zones = solver.data.get('config.zone')
        if not zones:
            # 섹션이 비어 있으면 이전 프로젝트 값이 남지 않도록 비운다
            ui.comboBox_name.blockSignals(True)
            self.zone_data.clear()
            ui.comboBox_name.clear()
            ui.comboBox_name.blockSignals(False)
            self.change_data(-1)
            return

        ui.comboBox_name.blockSignals(True)
        self.zone_data.clear()
        ui.comboBox_name.clear()

        for i, zone in enumerate(zones):
            d = ZoneData()
            d.comment = zone.get('_comment', f'zone_{i}')
            p1 = zone.get('p1', [0, 0])
            p2 = zone.get('p2', [0, 0])
            direction = zone.get('direction', [0, 1])
            d.p1 = [str(p1[0]), str(p1[1])]
            d.p2 = [str(p2[0]), str(p2[1])]
            d.direction = [str(direction[0]), str(direction[1])]
            d.length = str(zone.get('length', 1.0))
            d.zone_type = zone.get('zone_type', 'avoid_zone')
            d.k_avo = str(zone.get('K_avo', 200.0))
            d.avoid_radius = str(zone.get('avoid_radius', 15.0))
            d.outlet_id = str(zone.get('outlet_id', 0))
            d.grid = str(zone.get('grid', 1))
            d.raw_extra = {k: v for k, v in zone.items() if k not in _KNOWN_ZONE_KEYS}
            self.zone_data.append(d)
            ui.comboBox_name.addItem(d.comment)

        ui.comboBox_name.blockSignals(False)

        if self.zone_data:
            ui.comboBox_name.setCurrentIndex(0)
            self.change_data(0)

    def change_combo_text(self, combo, index, text):
        combo.blockSignals(True)
        combo.removeItem(index)
        combo.insertItem(index, text)
        combo.setCurrentIndex(index)
        combo.blockSignals(False)

    def remove_data(self):
        ui = self.ui
        index = ui.comboBox_name.currentIndex()
        if index == -1:
            return

        ui.comboBox_name.removeItem(index)
        del self.zone_data[index]

        self.change_data(index)

    def save_input_file(self, solver):
        for i, d in enumerate(self.zone_data):
            solver.add_zone(d.zone_type)

            solver.data.set(f'config.zone[{i}]._comment', d.comment)
            # add_zone이 심은 zone_type은 첫 zone에서만 뒤이은 set()에 지워진다.
            # (JsonTool.add가 리스트 첫 원소를 dict로 넣어, set의 인덱스 접근이 이를 비운다)
            solver.data.set(f'config.zone[{i}].zone_type', d.zone_type)

            # STL 형상으로 정의된 zone(mesh_path)은 사각형 좌표를 쓰지 않는다.
            # GUI에 mesh zone 편집 UI가 없어 p1/p2/direction/length가 기본값(0)으로
            # 남아 있으므로, 그대로 쓰면 원본의 형상 zone이 크기 0짜리 사각형 zone으로
            # 덮어써진다. raw_extra의 mesh_path는 아래에서 그대로 복원된다.
            if 'mesh_path' in getattr(d, 'raw_extra', {}):
                for key in ('p1', 'p2', 'direction', 'length'):
                    solver.data.remove(f'config.zone[{i}].{key}')
            else:
                solver.data.set(f'config.zone[{i}].p1[0]', float(d.p1[0]))
                solver.data.set(f'config.zone[{i}].p1[1]', float(d.p1[1]))
                solver.data.set(f'config.zone[{i}].p2[0]', float(d.p2[0]))
                solver.data.set(f'config.zone[{i}].p2[1]', float(d.p2[1]))
                solver.data.set(f'config.zone[{i}].direction[0]', float(d.direction[0]))
                solver.data.set(f'config.zone[{i}].direction[1]', float(d.direction[1]))
                solver.data.set(f'config.zone[{i}].length', float(d.length))

            solver.data.set(f'config.zone[{i}].grid', int(d.grid))

            if d.zone_type == 'avoid_zone':
                solver.data.set(f'config.zone[{i}].K_avo', float(d.k_avo))
                solver.data.set(f'config.zone[{i}].avoid_radius', float(d.avoid_radius))
            else:
                solver.data.set(f'config.zone[{i}].outlet_id', int(d.outlet_id))

            for k, v in getattr(d, 'raw_extra', {}).items():
                solver.data.set(f'config.zone[{i}].{k}', v)

        return solver
