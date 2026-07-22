from nextlib.utils.ui import load_ui
from view.panel.properties.report_ui import Ui_ReportForm


# 실제 솔버(RuntimeSPH2D)가 쓰는 result_report.items/flags 스키마 (S1~S5 실전 시나리오 기준).
# 여기 없는 키는 GUI가 모델링하지 않는 것으로 보고 raw_extra에 그대로 보존한다.
_KNOWN_ITEM_KEYS = {
    'pressure', 'density', 'rest_density', 'position', 'velocity', 'goal_position',
    'forward_vector', 'line_id', 'zone_id', 'outlet_id', 'path_field_id',
    'path_direction', 'path_direction_array', 'final_path_vector',
}
_KNOWN_FLAG_KEYS = {'zone', 'solid', 'path_solid'}


class ReportData:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 100.0
        self.time_interval = 0.02

        self.item_pressure = True
        self.item_density = True
        self.item_rest_density = True
        self.item_position = True
        self.item_velocity = True
        self.item_goal_position = True
        self.item_forward_vector = True
        self.item_line_id = True
        self.item_zone_id = True
        self.item_outlet_id = True
        self.item_path_field_id = True
        self.item_path_direction = True
        self.item_path_direction_array = False
        self.item_final_path_vector = True

        self.flag_zone = True
        self.flag_solid = True
        self.flag_path_solid = True


class ReportView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self.ui = load_ui(None, Ui_ReportForm).ui

        self.outlet_data = []
        # GUI가 모델링하지 않는 items/flags 키는 원본 그대로 보존 후 저장 시 재기록
        self._raw_extra_items = {}
        self._raw_extra_flags = {}
        self._initialize()

    def _initialize(self):
        ui = self.ui

    def get_widget(self):
        return self.ui.widget

    def save_input_file(self, solver):
        ui = self.ui

        solver.add_result_report()
        solver.data.set('config.result_report.save_start_time', float(ui.lineEdit_start_time.text()))
        solver.data.set('config.result_report.save_end_time', float(ui.lineEdit_end_time.text()))
        solver.data.set('config.result_report.save_time_interval', float(ui.lineEdit_time_interval.text()))

        solver.data.set('config.result_report.items.pressure', ui.checkBox_pressure.isChecked())
        solver.data.set('config.result_report.items.density', ui.checkBox_density.isChecked())
        solver.data.set('config.result_report.items.rest_density', ui.checkBox_rest_density.isChecked())
        solver.data.set('config.result_report.items.position', ui.checkBox_position.isChecked())
        solver.data.set('config.result_report.items.velocity', ui.checkBox_velocity.isChecked())
        solver.data.set('config.result_report.items.goal_position', ui.checkBox_goal_position.isChecked())
        solver.data.set('config.result_report.items.forward_vector', ui.checkBox_forward_vector.isChecked())
        solver.data.set('config.result_report.items.line_id', ui.checkBox_line_id.isChecked())
        solver.data.set('config.result_report.items.zone_id', ui.checkBox_zone_id.isChecked())
        solver.data.set('config.result_report.items.outlet_id', ui.checkBox_outlet_id.isChecked())
        solver.data.set('config.result_report.items.path_field_id', ui.checkBox_path_field_id.isChecked())
        solver.data.set('config.result_report.items.path_direction', ui.checkBox_path_direction.isChecked())
        solver.data.set('config.result_report.items.path_direction_array', ui.checkBox_path_direction_array.isChecked())
        solver.data.set('config.result_report.items.final_path_vector', ui.checkBox_final_path_vector.isChecked())

        solver.data.set('config.result_report.flags.zone', ui.checkBox_zone.isChecked())
        solver.data.set('config.result_report.flags.solid', ui.checkBox_solid.isChecked())
        solver.data.set('config.result_report.flags.path_solid', ui.checkBox_path_solid.isChecked())

        for k, v in self._raw_extra_items.items():
            solver.data.set(f'config.result_report.items.{k}', v)
        for k, v in self._raw_extra_flags.items():
            solver.data.set(f'config.result_report.flags.{k}', v)

        return solver

    def load_input_file(self, solver):
        ui = self.ui
        rr = solver.data.get('config.result_report')
        if not rr:
            return

        def s(key, default=''):
            v = rr.get(key)
            return str(v) if v is not None else str(default)

        ui.lineEdit_start_time.setText(s('save_start_time', '0.0'))
        ui.lineEdit_end_time.setText(s('save_end_time', '100'))
        ui.lineEdit_time_interval.setText(s('save_time_interval', '0.1'))

        items = rr.get('items', {})
        ui.checkBox_pressure.setChecked(bool(items.get('pressure', True)))
        ui.checkBox_density.setChecked(bool(items.get('density', True)))
        ui.checkBox_rest_density.setChecked(bool(items.get('rest_density', True)))
        ui.checkBox_position.setChecked(bool(items.get('position', True)))
        ui.checkBox_velocity.setChecked(bool(items.get('velocity', True)))
        ui.checkBox_goal_position.setChecked(bool(items.get('goal_position', True)))
        ui.checkBox_forward_vector.setChecked(bool(items.get('forward_vector', True)))
        ui.checkBox_line_id.setChecked(bool(items.get('line_id', True)))
        ui.checkBox_zone_id.setChecked(bool(items.get('zone_id', True)))
        ui.checkBox_outlet_id.setChecked(bool(items.get('outlet_id', True)))
        ui.checkBox_path_field_id.setChecked(bool(items.get('path_field_id', True)))
        ui.checkBox_path_direction.setChecked(bool(items.get('path_direction', True)))
        ui.checkBox_path_direction_array.setChecked(bool(items.get('path_direction_array', False)))
        ui.checkBox_final_path_vector.setChecked(bool(items.get('final_path_vector', True)))
        self._raw_extra_items = {k: v for k, v in items.items() if k not in _KNOWN_ITEM_KEYS}

        flags = rr.get('flags', {})
        ui.checkBox_zone.setChecked(bool(flags.get('zone', True)))
        ui.checkBox_solid.setChecked(bool(flags.get('solid', True)))
        ui.checkBox_path_solid.setChecked(bool(flags.get('path_solid', True)))
        self._raw_extra_flags = {k: v for k, v in flags.items() if k not in _KNOWN_FLAG_KEYS}
