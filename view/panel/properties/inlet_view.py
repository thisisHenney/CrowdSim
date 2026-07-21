from nextlib.utils.ui import load_ui
from view.panel.properties.inlet_ui import Ui_InletForm


_KNOWN_INLET_KEYS = {'name', 'type', 'exclude_outlets', 'p1', 'p2', 'velocity', 'dx',
                     'interval', 'start_time', 'end_time', 'material_index', 'grid', 'outlet_index'}


class InletData:
    def __init__(self):
        self.name = ''
        self.type = 'CROWD'
        self.exclude_outlets = []
        self.p1 = [0, 0]
        self.p2 = [0, 0]
        self.velocity = [0.0, 0.0]
        self.dx = 1
        self.interval = 100
        self.start_time = 0
        self.end_time = 0
        self.material_index = 0
        self.grid = 1
        self.outlet_index = -1
        self.raw_extra = {}


class InletView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.ui = load_ui(None, Ui_InletForm).ui

        self.inlet_data = []
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
        index = index if self.inlet_data and (0 <= index < len(self.inlet_data)) else (
            len(self.inlet_data) - 1 if len(self.inlet_data) > 0 else -1)

        if index == -1:
            ui.lineEdit_p1_x.setText('0')
            ui.lineEdit_p1_y.setText('0')
            ui.lineEdit_p2_x.setText('1')
            ui.lineEdit_p2_y.setText('1')

            ui.lineEdit_vel_x.setText('0')
            ui.lineEdit_vel_y.setText('0')
            ui.lineEdit_dx.setText('1')

            ui.lineEdit_interval.setText('100')
            ui.lineEdit_material_index.setText('0')
            ui.lineEdit_grid.setText('0')
            ui.lineEdit_outlet_index.setText('0')

        else:
            cur_data = self.inlet_data[index]

            ui.lineEdit_p1_x.setText(str(cur_data.p1[0]))
            ui.lineEdit_p1_y.setText(str(cur_data.p1[1]))
            ui.lineEdit_p2_x.setText(str(cur_data.p2[0]))
            ui.lineEdit_p2_y.setText(str(cur_data.p2[1]))

            ui.lineEdit_vel_x.setText(str(cur_data.velocity[0]))
            ui.lineEdit_vel_y.setText(str(cur_data.velocity[1]))
            ui.lineEdit_dx.setText(str(cur_data.dx))

            ui.lineEdit_interval.setText(str(cur_data.interval))
            ui.lineEdit_material_index.setText(str(cur_data.material_index))
            ui.lineEdit_grid.setText(str(cur_data.grid))
            ui.lineEdit_outlet_index.setText(str(cur_data.outlet_index))

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
            get_data = self.get_cur_data(InletData())

            self.inlet_data.append(get_data)
            ui.comboBox_name.addItem(get_data.name)
            ui.comboBox_name.setCurrentIndex(len(self.inlet_data) - 1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_name.currentText()

        get_data.p1[0] = ui.lineEdit_p1_x.text()
        get_data.p1[1] = ui.lineEdit_p1_y.text()
        get_data.p2[0] = ui.lineEdit_p2_x.text()
        get_data.p2[1] = ui.lineEdit_p2_y.text()

        get_data.velocity[0] = ui.lineEdit_vel_x.text()
        get_data.velocity[1] = ui.lineEdit_vel_y.text()
        get_data.dx = ui.lineEdit_dx.text()

        get_data.interval = ui.lineEdit_interval.text()
        get_data.material_index = ui.lineEdit_material_index.text()
        get_data.grid = ui.lineEdit_grid.text()
        get_data.outlet_index = ui.lineEdit_outlet_index.text()

        return get_data

    def save_data(self, index=-1):
        ui = self.ui

        if index == -1:
            index = ui.comboBox_name.currentIndex()

        cur_data = self.inlet_data[index]
        cur_data.name = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.name)
        self.get_cur_data(cur_data)

    def load_input_file(self, solver):
        ui = self.ui
        inlets = solver.data.get('config.inlet')
        if not inlets:
            return

        ui.comboBox_name.blockSignals(True)
        self.inlet_data.clear()
        ui.comboBox_name.clear()

        for i, inlet in enumerate(inlets):
            d = InletData()
            d.name = inlet.get('name', f'inlet_{i}')
            d.exclude_outlets = inlet.get('exclude_outlets', [])
            p1 = inlet.get('p1', [0, 0])
            p2 = inlet.get('p2', [0, 0])
            vel = inlet.get('velocity', [0.0, 0.0])
            d.p1 = [str(p1[0]), str(p1[1])]
            d.p2 = [str(p2[0]), str(p2[1])]
            d.velocity = [str(vel[0]), str(vel[1])]
            d.dx = str(inlet.get('dx', 1))
            d.interval = str(inlet.get('interval', 100))
            d.start_time = inlet.get('start_time', 0)
            d.end_time = inlet.get('end_time', 0)
            d.material_index = str(inlet.get('material_index', 0))
            d.grid = str(inlet.get('grid', 1))
            d.outlet_index = str(inlet.get('outlet_index', -1))
            d.raw_extra = {k: v for k, v in inlet.items() if k not in _KNOWN_INLET_KEYS}
            self.inlet_data.append(d)
            ui.comboBox_name.addItem(d.name)

        ui.comboBox_name.blockSignals(False)

        if self.inlet_data:
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
        del self.inlet_data[index]

        self.change_data(index)

    def save_input_file(self, solver):
        for i, d in enumerate(self.inlet_data):
            solver.add_inlet()

            solver.data.set(f'config.inlet[{i}].name', d.name)
            solver.data.set(f'config.inlet[{i}].exclude_outlets', getattr(d, 'exclude_outlets', []))

            solver.data.set(f'config.inlet[{i}].p1[0]', float(d.p1[0]))
            solver.data.set(f'config.inlet[{i}].p1[1]', float(d.p1[1]))
            solver.data.set(f'config.inlet[{i}].p2[0]', float(d.p2[0]))
            solver.data.set(f'config.inlet[{i}].p2[1]', float(d.p2[1]))

            solver.data.set(f'config.inlet[{i}].velocity[0]', float(d.velocity[0]))
            solver.data.set(f'config.inlet[{i}].velocity[1]', float(d.velocity[1]))
            solver.data.set(f'config.inlet[{i}].dx', int(d.dx))

            solver.data.set(f'config.inlet[{i}].interval', int(d.interval))
            solver.data.set(f'config.inlet[{i}].start_time', getattr(d, 'start_time', 0))
            solver.data.set(f'config.inlet[{i}].end_time', getattr(d, 'end_time', 0))
            solver.data.set(f'config.inlet[{i}].material_index', int(d.material_index))
            solver.data.set(f'config.inlet[{i}].grid', int(d.grid))
            solver.data.set(f'config.inlet[{i}].outlet_index', int(d.outlet_index))

            for k, v in getattr(d, 'raw_extra', {}).items():
                solver.data.set(f'config.inlet[{i}].{k}', v)

        return solver
