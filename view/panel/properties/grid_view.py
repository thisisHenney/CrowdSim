from nextlib.utils.ui import load_ui
from view.panel.properties.grid_ui import Ui_GridForm


class GridData:
    def __init__(self):
        self.name = ''

        self.domain_min = [-1, -1]
        self.domain_max = [1, 1]
        self.width = -1
        self.max_particle = 10000


class GridView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.ui = load_ui(None, Ui_GridForm).ui

        self.grid_data = []

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

        index = index if self.grid_data and (0 <= index < len(self.grid_data)) else (
            len(self.grid_data) - 1 if len(self.grid_data) > 0 else -1)

        if index == -1:
            ui.lineEdit_min_x.setText('')
            ui.lineEdit_min_y.setText('')
            ui.lineEdit_max_x.setText('')
            ui.lineEdit_max_y.setText('')

            ui.lineEdit_width.setText('')
            ui.lineEdit_max_particle.setText('')

        else:
            cur_data = self.grid_data[index]

            ui.lineEdit_min_x.setText(str(cur_data.domain_min[0]))
            ui.lineEdit_min_y.setText(str(cur_data.domain_min[1]))
            ui.lineEdit_max_x.setText(str(cur_data.domain_max[0]))
            ui.lineEdit_max_y.setText(str(cur_data.domain_max[1]))

            ui.lineEdit_width.setText(str(cur_data.width))
            ui.lineEdit_max_particle.setText(str(cur_data.max_particle))

    def _clicked_add(self):
        self.add_data()
        if hasattr(self._parent, '_load_background_map'):
            self._parent._load_background_map()

    def _clicked_save(self):
        self.save_data()
        if hasattr(self._parent, '_load_background_map'):
            self._parent._load_background_map()

    def _clicked_remove(self):
        self.remove_data()

    def get_widget(self):
        return self.ui.widget

    def add_data(self):
        ui = self.ui

        name = ui.comboBox_name.currentText()
        if name:
            get_data = self.get_cur_data(GridData())

            self.grid_data.append(get_data)
            ui.comboBox_name.addItem(get_data.name)
            ui.comboBox_name.setCurrentIndex(len(self.grid_data)-1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_name.currentText()
        get_data.domain_min[0] = ui.lineEdit_min_x.text()
        get_data.domain_min[1] = ui.lineEdit_min_y.text()
        get_data.domain_max[0] = ui.lineEdit_max_x.text()
        get_data.domain_max[1] = ui.lineEdit_max_y.text()
        get_data.width = ui.lineEdit_width.text()
        get_data.max_particle = ui.lineEdit_max_particle.text()

        return get_data

    def save_data(self, index=-1):
        ui = self.ui

        if index == -1:
            index = ui.comboBox_name.currentIndex()

        cur_data = self.grid_data[index]
        cur_data.name = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.name)
        self.get_cur_data(cur_data)

    def remove_data(self):
        ui = self.ui
        index = ui.comboBox_name.currentIndex()
        if index == -1:
            return

        ui.comboBox_name.removeItem(index)
        del self.grid_data[index]

        # if len(self.grid_data) == 0:
        #     ui.lineEdit_min_x.setDisabled(True)
        #     ui.lineEdit_min_y.setDisabled(True)
        #     ui.lineEdit_max_x.setDisabled(True)
        #     ui.lineEdit_max_y.setDisabled(True)
        #     ui.lineEdit_width.setDisabled(True)
        #     ui.lineEdit_max_particle.setDisabled(True)

        self.change_data(index)

    def save_input_file(self, solver):
        for i, d in enumerate(self.grid_data):
            solver.add_grid(d.name)
            solver.data.set(f'config.grid[{i}].domain.min[0]', float(d.domain_min[0]))
            solver.data.set(f'config.grid[{i}].domain.min[1]', float(d.domain_min[1]))
            solver.data.set(f'config.grid[{i}].domain.min[2]', 1)
            solver.data.set(f'config.grid[{i}].domain.max[0]', float(d.domain_max[0]))
            solver.data.set(f'config.grid[{i}].domain.max[1]', float(d.domain_max[1]))
            solver.data.set(f'config.grid[{i}].domain.max[2]', 1)

            solver.data.set(f'config.grid[{i}].width', int(d.width))
            solver.data.set(f'config.grid[{i}].max_particle', int(d.max_particle))

        return solver

    def load_input_file(self, solver):
        ui = self.ui
        grids = solver.data.get('config.grid')
        if not grids:
            return

        ui.comboBox_name.blockSignals(True)
        self.grid_data.clear()
        ui.comboBox_name.clear()

        for g in grids:
            d = GridData()
            d.name = str(g.get('name', ''))
            domain = g.get('domain', {})
            mn = domain.get('min', [-1, -1])
            mx = domain.get('max', [1, 1])
            d.domain_min = [str(mn[0]), str(mn[1])]
            d.domain_max = [str(mx[0]), str(mx[1])]
            d.width = str(g.get('width', -1))
            d.max_particle = str(g.get('max_particle', 10000))
            self.grid_data.append(d)
            ui.comboBox_name.addItem(d.name)

        ui.comboBox_name.blockSignals(False)

        if self.grid_data:
            ui.comboBox_name.setCurrentIndex(0)
            self.change_data(0)

    def change_combo_text(self, combo, index, text):
        combo.blockSignals(True)
        combo.removeItem(index)
        combo.insertItem(index, text)
        combo.setCurrentIndex(index)
        combo.blockSignals(False)
