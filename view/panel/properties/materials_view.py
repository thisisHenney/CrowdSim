from nextlib.utils.ui import load_ui
from view.panel.properties.material_ui import Ui_MaterialsForm
from view.panel.properties import _extra_ui


_KNOWN_MATERIAL_KEYS = {'name', 'is_main_material', 'rho_min', 'rho_max', 'mu', 'outlet_id'}


_EDIT_FIELDS = (
    'checkBox_main',
    'lineEdit_rho_min',
    'lineEdit_rho_max',
    'lineEdit_mu',
    'lineEdit_outlet_id',
    # 항목이 없으면 저장/삭제도 대상이 없다.
    # ('추가'는 잠그지 않는다 - 첫 항목을 만드는 유일한 길이다)
    'pushButton_save',
    'pushButton_remove',
)


class MaterialData:
    def __init__(self):
        self.name = ''

        self.is_main = False
        self.rho_min = 0
        self.rho_max = 5
        self.mu = 0.0
        self.outlet_id = 0
        self.raw_extra = {}


class MaterialsView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.ui = load_ui(None, Ui_MaterialsForm).ui

        self.material_data = []

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
        if not (0 <= index < len(self.material_data)):
            return
        self.get_cur_data(self.material_data[index])
        parent = getattr(self, '_parent', None)
        if parent is not None and hasattr(parent, 'set_dirty'):
            parent.set_dirty(True)

    def change_data(self, index):
        self._filling = True
        try:
            ui = self.ui

            index = index if self.material_data and (0 <= index < len(self.material_data)) else (len(self.material_data) - 1 if len(self.material_data) > 0 else -1)

            if index == -1:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)
                ui.checkBox_main.setChecked(False)
                ui.lineEdit_rho_min.setText('')
                ui.lineEdit_rho_max.setText('')
                ui.lineEdit_mu.setText('')
                ui.lineEdit_outlet_id.setText('')

            else:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, True)
                cur_data = self.material_data[index]

                ui.checkBox_main.setChecked(cur_data.is_main)
                ui.lineEdit_rho_min.setText(str(cur_data.rho_min))
                ui.lineEdit_rho_max.setText(str(cur_data.rho_max))
                ui.lineEdit_mu.setText(str(cur_data.mu))
                ui.lineEdit_outlet_id.setText(str(cur_data.outlet_id))
        finally:
            self._filling = False

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
            get_data = self.get_cur_data(MaterialData())

            self.material_data.append(get_data)
            ui.comboBox_name.addItem(get_data.name)
            ui.comboBox_name.setCurrentIndex(len(self.material_data) - 1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_name.currentText()
        get_data.is_main = ui.checkBox_main.isChecked()
        get_data.rho_min = ui.lineEdit_rho_min.text()
        get_data.rho_max = ui.lineEdit_rho_max.text()
        get_data.mu = ui.lineEdit_mu.text()
        get_data.outlet_id = ui.lineEdit_outlet_id.text()
        return get_data

    def save_data(self, index=-1):
        ui = self.ui

        if index == -1:
            index = ui.comboBox_name.currentIndex()

        cur_data = self.material_data[index]
        cur_data.name = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.name)
        self.get_cur_data(cur_data)

    def remove_data(self):
        ui = self.ui
        index = ui.comboBox_name.currentIndex()
        if index == -1:
            return

        ui.comboBox_name.removeItem(index)
        del self.material_data[index]

        self.change_data(index)

    def save_input_file(self, solver):
        for i, d in enumerate(self.material_data):
            solver.add_material(d.name)

            solver.data.set(f'config.materials[{i}].is_main_material', d.is_main)
            solver.data.set(f'config.materials[{i}].rho_min', int(d.rho_min))
            solver.data.set(f'config.materials[{i}].rho_max', int(d.rho_max))
            solver.data.set(f'config.materials[{i}].mu', float(d.mu))
            solver.data.set(f'config.materials[{i}].outlet_id', int(d.outlet_id))

            for k, v in getattr(d, 'raw_extra', {}).items():
                solver.data.set(f'config.materials[{i}].{k}', v)

        return solver

    def load_input_file(self, solver):
        ui = self.ui
        materials = solver.data.get('config.materials')
        if not materials:
            # 섹션이 비어 있으면 이전 프로젝트 값이 남지 않도록 비운다
            ui.comboBox_name.blockSignals(True)
            self.material_data.clear()
            ui.comboBox_name.clear()
            ui.comboBox_name.blockSignals(False)
            self.change_data(-1)
            return

        ui.comboBox_name.blockSignals(True)
        self.material_data.clear()
        ui.comboBox_name.clear()

        for m in materials:
            d = MaterialData()
            d.name = str(m.get('name', ''))
            d.is_main = bool(m.get('is_main_material', False))
            d.rho_min = str(m.get('rho_min', 0))
            d.rho_max = str(m.get('rho_max', 5))
            d.mu = str(m.get('mu', 0.0))
            d.outlet_id = str(m.get('outlet_id', -1))
            d.raw_extra = {k: v for k, v in m.items() if k not in _KNOWN_MATERIAL_KEYS}
            self.material_data.append(d)
            ui.comboBox_name.addItem(d.name)

        ui.comboBox_name.blockSignals(False)

        if self.material_data:
            ui.comboBox_name.setCurrentIndex(0)
            self.change_data(0)

    def change_combo_text(self, combo, index, text):
        combo.blockSignals(True)
        combo.removeItem(index)
        combo.insertItem(index, text)
        combo.setCurrentIndex(index)
        combo.blockSignals(False)
