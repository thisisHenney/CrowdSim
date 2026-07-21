from nextlib.utils.ui import load_ui
from view.panel.properties.material_ui import Ui_MaterialsForm


_KNOWN_MATERIAL_KEYS = {'name', 'is_main_material', 'rho_min', 'rho_max', 'mu', 'outlet_id'}


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

    def _changed_combo_name(self, index):
        if index == -1:
            return

        self.change_data(index)

    def change_data(self, index):
        ui = self.ui

        index = index if self.material_data and (0 <= index < len(self.material_data)) else (len(self.material_data) - 1 if len(self.material_data) > 0 else -1)

        if index == -1:
            ui.checkBox_main.setChecked(False)
            ui.lineEdit_rho_min.setText('')
            ui.lineEdit_rho_max.setText('')
            ui.lineEdit_mu.setText('')
            ui.lineEdit_outlet_id.setText('')

        else:
            cur_data = self.material_data[index]

            ui.checkBox_main.setChecked(cur_data.is_main)
            ui.lineEdit_rho_min.setText(str(cur_data.rho_min))
            ui.lineEdit_rho_max.setText(str(cur_data.rho_max))
            ui.lineEdit_mu.setText(str(cur_data.mu))
            ui.lineEdit_outlet_id.setText(str(cur_data.outlet_id))

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
