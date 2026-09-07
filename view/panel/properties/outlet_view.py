from PySide6.QtWidgets import QCheckBox

from nextlib.utils.ui import load_ui
from view.panel.properties.outlet_ui import Ui_OutletForm
from view.panel.properties import _extra_ui


_KNOWN_OUTLET_KEYS = {'name', 'num', 'is_erase', 'type', 'p1', 'p2', 'grid',
                      'settle_radius', 'sig_k', 'sig_x'}


_EDIT_FIELDS = (
    'radioButton_point',
    'radioButton_line',
    'checkBox_is_erase',
    'lineEdit_p_x',
    'lineEdit_p_y',
    'lineEdit_p1_x',
    'lineEdit_p1_y',
    'lineEdit_p2_x',
    'lineEdit_p2_y',
    'lineEdit_grid',
    'lineEdit_settle_radius',
    'lineEdit_sig_k',
    'lineEdit_sig_x',
    # 항목이 없으면 저장/삭제도 대상이 없다.
    # ('추가'는 잠그지 않는다 - 첫 항목을 만드는 유일한 길이다)
    'pushButton_save',
    'pushButton_remove',
)


class OutletData:
    def __init__(self):
        self.name = 'outlet'
        self.num = 0
        self.is_erase = False
        self.is_point = True
        self.p = [0, 0]
        self.p1 = [0, 0]
        self.p2 = [0, 0]
        self.grid = 1
        self.settle_radius = None
        self.sig_k = None
        self.sig_x = None
        self.raw_extra = {}


class OutletView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.ui = load_ui(None, Ui_OutletForm).ui

        self.outlet_data = []
        self._initialize()

    def _initialize(self):
        ui = self.ui

        ui.comboBox_name.currentIndexChanged.connect(self._changed_combo_name)
        ui.pushButton_add.clicked.connect(self._clicked_add)
        ui.pushButton_save.clicked.connect(self._clicked_save)
        ui.pushButton_remove.clicked.connect(self._clicked_remove)

        self._build_extra_fields()

        # 목록이 비어 있는 초기 상태에서는 입력란을 잠가 둔다.
        # ('추가'를 눌러 항목이 생기면 change_data()가 다시 켠다)
        _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)

    def _build_extra_fields(self):
        """uic 출력에 없는 입력란을 덧붙인다 (is_erase / grid / 정착·시그모이드)."""
        ui = self.ui

        ui.checkBox_is_erase = QCheckBox('통과한 입자를 제거 (is_erase)')
        ui.lineEdit_grid = _extra_ui.make_edit(width=80)
        ui.lineEdit_settle_radius = _extra_ui.make_edit(width=80, placeholder='미사용')
        ui.lineEdit_sig_k = _extra_ui.make_edit(width=80, placeholder='미사용')
        ui.lineEdit_sig_x = _extra_ui.make_edit(width=80, placeholder='미사용')

        lay = ui.verticalLayout_5
        lay.addWidget(ui.checkBox_is_erase)
        lay.addWidget(_extra_ui.make_row('Grid', ui.lineEdit_grid, stretch_last=False))
        lay.addWidget(_extra_ui.make_row('정착 반경', ui.lineEdit_settle_radius,
                                         stretch_last=False))
        lay.addWidget(_extra_ui.make_row('sig_k / sig_x', ui.lineEdit_sig_k,
                                         ui.lineEdit_sig_x, stretch_last=False))

    def _changed_combo_name(self, index):
        if index == -1:
            return
        self.change_data(index)

    def change_data(self, index):
        ui = self.ui
        index = index if self.outlet_data and (0 <= index < len(self.outlet_data)) else (
            len(self.outlet_data) - 1 if len(self.outlet_data) > 0 else -1)

        if index == -1:
            _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)
            ui.radioButton_point.setChecked(True)
            ui.radioButton_line.setChecked(False)
            ui.lineEdit_p_x.setText('0')
            ui.lineEdit_p_y.setText('0')
            ui.lineEdit_p1_x.setText('0')
            ui.lineEdit_p1_y.setText('0')
            ui.lineEdit_p2_x.setText('1')
            ui.lineEdit_p2_y.setText('1')
            ui.checkBox_is_erase.setChecked(False)
            ui.lineEdit_grid.setText('1')
            ui.lineEdit_settle_radius.setText('')
            ui.lineEdit_sig_k.setText('')
            ui.lineEdit_sig_x.setText('')

        else:
            _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, True)
            cur_data = self.outlet_data[index]

            ui.radioButton_point.setChecked(cur_data.is_point)
            ui.radioButton_line.setChecked(not cur_data.is_point)
            ui.lineEdit_p_x.setText(str(cur_data.p[0]))
            ui.lineEdit_p_y.setText(str(cur_data.p[1]))
            ui.lineEdit_p1_x.setText(str(cur_data.p1[0]))
            ui.lineEdit_p1_y.setText(str(cur_data.p1[1]))
            ui.lineEdit_p2_x.setText(str(cur_data.p2[0]))
            ui.lineEdit_p2_y.setText(str(cur_data.p2[1]))
            ui.checkBox_is_erase.setChecked(bool(cur_data.is_erase))
            ui.lineEdit_grid.setText(str(cur_data.grid))
            ui.lineEdit_settle_radius.setText(_extra_ui.format_num(cur_data.settle_radius))
            ui.lineEdit_sig_k.setText(_extra_ui.format_num(cur_data.sig_k))
            ui.lineEdit_sig_x.setText(_extra_ui.format_num(cur_data.sig_x))

    def _clicked_add(self):
        self.add_data()

    def _clicked_save(self):
        self.save_data()

    def _clicked_remove(self):
        self.remove_data()

    def get_widget(self):
        return self.ui.widget

    def add_data(self):
        ui = self.ui

        name = ui.comboBox_name.currentText()
        if name:
            get_data = self.get_cur_data(OutletData())

            self.outlet_data.append(get_data)
            ui.comboBox_name.addItem(get_data.name)
            ui.comboBox_name.setCurrentIndex(len(self.outlet_data) - 1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_name.currentText()

        get_data.is_point = ui.radioButton_point.isChecked()

        get_data.p[0] = ui.lineEdit_p_x.text()
        get_data.p[1] = ui.lineEdit_p_y.text()
        get_data.p1[0] = ui.lineEdit_p1_x.text()
        get_data.p1[1] = ui.lineEdit_p1_y.text()
        get_data.p2[0] = ui.lineEdit_p2_x.text()
        get_data.p2[1] = ui.lineEdit_p2_y.text()

        get_data.is_erase = ui.checkBox_is_erase.isChecked()
        get_data.grid = _extra_ui.parse_num(ui.lineEdit_grid.text(), 1)
        get_data.settle_radius = _extra_ui.parse_num(ui.lineEdit_settle_radius.text())
        get_data.sig_k = _extra_ui.parse_num(ui.lineEdit_sig_k.text())
        get_data.sig_x = _extra_ui.parse_num(ui.lineEdit_sig_x.text())

        return get_data

    def save_data(self, index=-1):
        ui = self.ui

        if index == -1:
            index = ui.comboBox_name.currentIndex()

        cur_data = self.outlet_data[index]
        cur_data.name = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.name)
        self.get_cur_data(cur_data)

    def load_input_file(self, solver):
        ui = self.ui
        outlets = solver.data.get('config.outlet')
        if not outlets:
            # 섹션이 비어 있으면 이전 프로젝트 값이 남지 않도록 비운다
            ui.comboBox_name.blockSignals(True)
            self.outlet_data.clear()
            ui.comboBox_name.clear()
            ui.comboBox_name.blockSignals(False)
            self.change_data(-1)
            return

        ui.comboBox_name.blockSignals(True)
        self.outlet_data.clear()
        ui.comboBox_name.clear()

        for i, outlet in enumerate(outlets):
            d = OutletData()
            d.name = outlet.get('name', f'outlet_{i}')
            d.num = outlet.get('num', i)
            d.is_erase = outlet.get('is_erase', False)
            d.is_point = outlet.get('type', 'point') == 'point'
            if d.is_point:
                p1 = outlet.get('p1', [0, 0])
                d.p = [str(p1[0]), str(p1[1])]
            else:
                p1 = outlet.get('p1', [0, 0])
                p2 = outlet.get('p2', [0, 0])
                d.p1 = [str(p1[0]), str(p1[1])]
                d.p2 = [str(p2[0]), str(p2[1])]
            d.grid = outlet.get('grid', 1)
            d.settle_radius = outlet.get('settle_radius')
            d.sig_k = outlet.get('sig_k')
            d.sig_x = outlet.get('sig_x')
            d.raw_extra = {k: v for k, v in outlet.items() if k not in _KNOWN_OUTLET_KEYS}
            self.outlet_data.append(d)
            ui.comboBox_name.addItem(d.name)

        ui.comboBox_name.blockSignals(False)

        if self.outlet_data:
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
        del self.outlet_data[index]

        self.change_data(index)

    def save_input_file(self, solver):
        for i, d in enumerate(self.outlet_data):
            # num은 목록 순서를 그대로 쓴다(0부터). zone.outlet_id/inlet.exclude_outlets가
            # 이 번호로 출구를 지목하므로 목록 위치와 반드시 일치해야 한다. 예전엔
            # `getattr(d, 'num', i)`였는데 OutletData가 num을 항상 0으로 초기화하고
            # 위젯도 없어서 폴백이 결코 동작하지 않았고, 그 결과 GUI로 만든 케이스는
            # 모든 출구가 num=0이었다.
            d.num = i
            solver.add_outlet(d.is_point, num=i)
            solver.data.set(f'config.outlet[{i}].name', getattr(d, 'name', 'outlet'))
            solver.data.set(f'config.outlet[{i}].num', i)
            solver.data.set(f'config.outlet[{i}].is_erase', getattr(d, 'is_erase', False))
            if d.is_point:
                solver.data.set(f'config.outlet[{i}].p1[0]', float(d.p[0]))
                solver.data.set(f'config.outlet[{i}].p1[1]', float(d.p[1]))
            else:
                solver.data.set(f'config.outlet[{i}].p1[0]', float(d.p1[0]))
                solver.data.set(f'config.outlet[{i}].p1[1]', float(d.p1[1]))
                solver.data.set(f'config.outlet[{i}].p2[0]', float(d.p2[0]))
                solver.data.set(f'config.outlet[{i}].p2[1]', float(d.p2[1]))
            solver.data.set(f'config.outlet[{i}].grid', getattr(d, 'grid', 1))

            # 원래 없던 키가 저장만으로 새로 생기지 않도록 값이 있을 때만 쓴다.
            # 다만 선(line) 출구의 sig_k/sig_x는 예외로 항상 쓴다 — 이 두 키가
            # 없으면 솔버가 메시지 한 줄 없이 즉시 죽는다(0xC0000409).
            for key in ('settle_radius', 'sig_k', 'sig_x'):
                value = getattr(d, key, None)
                if value is None and not d.is_point and key in ('sig_k', 'sig_x'):
                    value = 0.0
                if value is not None:
                    solver.data.set(f'config.outlet[{i}].{key}', value)

            for k, v in getattr(d, 'raw_extra', {}).items():
                solver.data.set(f'config.outlet[{i}].{k}', v)

        return solver
