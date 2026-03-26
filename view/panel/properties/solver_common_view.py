from nextlib.utils.ui import load_ui
from view.panel.properties.solver_common_ui import Ui_SolverCommonForm


class SolverCommonView:
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self.ui = load_ui(None, Ui_SolverCommonForm).ui

        self._initialize()

    def _initialize(self):
        ...

    def get_widget(self):
        return self.ui.widget

    def save_input_file(self, solver):
        ui = self.ui

        solver.data.set('config.solver_common.solver_type', ui.lineEdit_type.text())
        solver.data.set('config.solver_common.simulation_start_time', float(ui.lineEdit_12.text()))
        solver.data.set('config.solver_common.simulation_end_time', float(ui.lineEdit_13.text()))
        solver.data.set('config.solver_common.time_step', float(ui.lineEdit_14.text()))

        solver.data.set('config.solver_common.radius', float(ui.lineEdit_15.text()))
        solver.data.set('config.solver_common.H', float(ui.lineEdit_16.text()))

        solver.data.set('config.solver_common.s_pref', float(ui.lineEdit_17.text()))
        solver.data.set('config.solver_common.s_max', float(ui.lineEdit_18.text()))
        solver.data.set('config.solver_common.a_max', float(ui.lineEdit_19.text()))

        solver.data.set('config.solver_common.K_obs', float(ui.lineEdit_20.text()))
        solver.data.set('config.solver_common.K_ag', float(ui.lineEdit_21.text()))
        solver.data.set('config.solver_common.K_goal', float(ui.lineEdit_22.text()))

        solver.data.set('config.solver_common.tau', float(ui.lineEdit_23.text()))
        solver.data.set('config.solver_common.V_0', float(ui.lineEdit_24.text()))
        solver.data.set('config.solver_common.sigma', float(ui.lineEdit_25.text()))
        solver.data.set('config.solver_common.T', float(ui.lineEdit_26.text()))
        solver.data.set('config.solver_common.U_0', float(ui.lineEdit_27.text()))
        solver.data.set('config.solver_common.R', float(ui.lineEdit_28.text()))

        solver.data.set('config.solver_common.w', float(ui.lineEdit_29.text()))
        solver.data.set('config.solver_common.k', float(ui.lineEdit_30.text()))
        solver.data.set('config.solver_common.T_p', float(ui.lineEdit_31.text()))

        solver.data.set('config.solver_common.blending.is_blending', ui.checkBox_is_blending.isChecked())
        solver.data.set('config.solver_common.blending.collision_avoidance', ui.comboBox_collision_avoidance.currentText())
        solver.data.set('config.solver_common.blending.collision_density', float(ui.doubleSpinBox_collision_density.value()))
        solver.data.set('config.solver_common.blending.sph_density', float(ui.doubleSpinBox_sph_density.value()))

        solver.data.set('config.solver_common.initial_velocity[0]', float(ui.lineEdit_32.text()))
        solver.data.set('config.solver_common.initial_velocity[1]', float(ui.lineEdit_33.text()))

        # solver.data.set('config.solver_common.goal_position[0]', 0)
        # solver.data.set('config.solver_common.goal_position[1]', -12)

        solver.data.set('config.solver_common.devices[0]', float(ui.lineEdit_36.text()))

        return solver

    def load_input_file(self, solver):
        ui = self.ui
        sc = 'config.solver_common'

        def g(key, default=''):
            v = solver.data.get(key)
            return str(v) if v is not None else str(default)

        ui.lineEdit_type.setText(g(f'{sc}.solver_type', 'CROWD'))
        ui.lineEdit_12.setText(g(f'{sc}.simulation_start_time', '0.0'))
        ui.lineEdit_13.setText(g(f'{sc}.simulation_end_time', '20.0'))
        ui.lineEdit_14.setText(g(f'{sc}.time_step', '0.02'))

        ui.lineEdit_15.setText(g(f'{sc}.radius', '0.25'))
        ui.lineEdit_16.setText(g(f'{sc}.H', '1'))

        ui.lineEdit_17.setText(g(f'{sc}.s_pref', '1.4'))
        ui.lineEdit_18.setText(g(f'{sc}.s_max', '1.8'))
        ui.lineEdit_19.setText(g(f'{sc}.a_max', '9999999999.9'))

        ui.lineEdit_20.setText(g(f'{sc}.K_obs', '200.0'))
        ui.lineEdit_21.setText(g(f'{sc}.K_ag', '50.0'))
        ui.lineEdit_22.setText(g(f'{sc}.K_goal', '1.0'))

        ui.lineEdit_23.setText(g(f'{sc}.tau', '0.5'))
        ui.lineEdit_24.setText(g(f'{sc}.V_0', '2.1'))
        ui.lineEdit_25.setText(g(f'{sc}.sigma', '0.3'))
        ui.lineEdit_26.setText(g(f'{sc}.T', '2.0'))
        ui.lineEdit_27.setText(g(f'{sc}.U_0', '2.1'))
        ui.lineEdit_28.setText(g(f'{sc}.R', '0.1'))

        ui.lineEdit_29.setText(g(f'{sc}.w', '1.0'))
        ui.lineEdit_30.setText(g(f'{sc}.k', '200.0'))
        ui.lineEdit_31.setText(g(f'{sc}.T_p', '0.1'))

        is_blending = solver.data.get(f'{sc}.blending.is_blending')
        ui.checkBox_is_blending.setChecked(bool(is_blending) if is_blending is not None else True)

        ca = solver.data.get(f'{sc}.blending.collision_avoidance')
        if ca:
            ui.comboBox_collision_avoidance.setCurrentText(str(ca))

        cd = solver.data.get(f'{sc}.blending.collision_density')
        if cd is not None:
            ui.doubleSpinBox_collision_density.setValue(float(cd))

        sd = solver.data.get(f'{sc}.blending.sph_density')
        if sd is not None:
            ui.doubleSpinBox_sph_density.setValue(float(sd))

        ui.lineEdit_32.setText(g(f'{sc}.initial_velocity[0]', '0'))
        ui.lineEdit_33.setText(g(f'{sc}.initial_velocity[1]', '0'))

        ui.lineEdit_36.setText(g(f'{sc}.devices[0]', '0'))
