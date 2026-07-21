from nextlib.utils.ui import load_ui
from view.panel.properties.zone_ui import Ui_ZoneForm


_KNOWN_ZONE_KEYS = {'_comment', 'p1', 'p2', 'direction', 'length', 'zone_type',
                    'K_avo', 'avoid_radius', 'outlet_id', 'grid'}


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

    def _changed_combo_name(self, index):
        if index == -1:
            return
        self.change_data(index)

    def change_data(self, index):
        ui = self.ui
        index = index if self.zone_data and (0 <= index < len(self.zone_data)) else (
            len(self.zone_data) - 1 if len(self.zone_data) > 0 else -1)

        if index == -1:
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
