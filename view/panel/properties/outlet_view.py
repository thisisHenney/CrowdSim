from nextlib.utils.ui import load_ui
from view.panel.properties.outlet_ui import Ui_OutletForm


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

    def _changed_combo_name(self, index):
        if index == -1:
            return
        self.change_data(index)

    def change_data(self, index):
        ui = self.ui
        index = index if self.outlet_data and (0 <= index < len(self.outlet_data)) else (
            len(self.outlet_data) - 1 if len(self.outlet_data) > 0 else -1)

        if index == -1:
            ui.radioButton_point.setChecked(True)
            ui.radioButton_line.setChecked(False)
            ui.lineEdit_p_x.setText('0')
            ui.lineEdit_p_y.setText('0')
            ui.lineEdit_p1_x.setText('0')
            ui.lineEdit_p1_y.setText('0')
            ui.lineEdit_p2_x.setText('1')
            ui.lineEdit_p2_y.setText('1')

        else:
            cur_data = self.outlet_data[index]

            ui.radioButton_point.setChecked(cur_data.is_point)
            ui.radioButton_line.setChecked(not cur_data.is_point)
            ui.lineEdit_p_x.setText(str(cur_data.p[0]))
            ui.lineEdit_p_y.setText(str(cur_data.p[1]))
            ui.lineEdit_p1_x.setText(str(cur_data.p1[0]))
            ui.lineEdit_p1_y.setText(str(cur_data.p1[1]))
            ui.lineEdit_p2_x.setText(str(cur_data.p2[0]))
            ui.lineEdit_p2_y.setText(str(cur_data.p2[1]))

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
            solver.add_outlet(d.is_point, num=getattr(d, 'num', i))
            solver.data.set(f'config.outlet[{i}].name', getattr(d, 'name', 'outlet'))
            solver.data.set(f'config.outlet[{i}].num', getattr(d, 'num', i))
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

        return solver
