from nextlib.utils.ui import load_ui
from view.panel.properties.report_ui import Ui_ReportForm


class ReportData:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 100.0
        self.time_interval = 0.02

        self.item_pressure = True
        self.item_density = True
        self.item_restDensity = True
        self.item_position = True
        self.item_velocity = True
        self.item_goal_position = True
        self.item_adjoint = True
        self.item_prt_idx = True
        self.item_forward_vector = True
        self.item_line_id = True
        self.item_acceleration_collision = True
        self.flags_path_goal_point = True
        self.flags_path_solid = True


class ReportView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self.ui = load_ui(None, Ui_ReportForm).ui

        self.outlet_data = []
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
        solver.data.set('config.result_report.items.restDensity', ui.checkBox_restDensity.isChecked())
        solver.data.set('config.result_report.items.position', ui.checkBox_position.isChecked())
        solver.data.set('config.result_report.items.velocity', ui.checkBox_velocity.isChecked())
        solver.data.set('config.result_report.items.goal_position', ui.checkBox_goal_position.isChecked())
        solver.data.set('config.result_report.items.adjoint', ui.checkBox_adjoint.isChecked())
        solver.data.set('config.result_report.items.prt_idx', ui.checkBox_prt_idx.isChecked())
        solver.data.set('config.result_report.items.forward_vector', ui.checkBox_forward_vector.isChecked())
        solver.data.set('config.result_report.items.line_id', ui.checkBox_line_id.isChecked())
        solver.data.set('config.result_report.items.acceleration_collision', ui.checkBox_acceleration_collision.isChecked())

        solver.data.set('config.result_report.flags.path_goal_point', ui.checkBox_path_goal_point.isChecked())
        solver.data.set('config.result_report.flags.path_solid', ui.checkBox_path_solid.isChecked())

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
        ui.checkBox_restDensity.setChecked(bool(items.get('restDensity', True)))
        ui.checkBox_position.setChecked(bool(items.get('position', True)))
        ui.checkBox_velocity.setChecked(bool(items.get('velocity', True)))
        ui.checkBox_goal_position.setChecked(bool(items.get('goal_position', True)))
        ui.checkBox_adjoint.setChecked(bool(items.get('adjoint', True)))
        ui.checkBox_prt_idx.setChecked(bool(items.get('prt_idx', True)))
        ui.checkBox_forward_vector.setChecked(bool(items.get('forward_vector', True)))
        ui.checkBox_line_id.setChecked(bool(items.get('line_id', True)))
        ui.checkBox_acceleration_collision.setChecked(bool(items.get('acceleration_collision', True)))

        flags = rr.get('flags', {})
        ui.checkBox_path_goal_point.setChecked(bool(flags.get('path_goal_point', False)))
        ui.checkBox_path_solid.setChecked(bool(flags.get('path_solid', False)))
