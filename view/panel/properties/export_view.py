from nextlib.utils.ui import load_ui
from view.panel.properties.export_ui import Ui_ExportForm


class ExportView:
    def __init__(self, parent):
        self._parent = parent

        self.ui = load_ui(None, Ui_ExportForm).ui

        self.outlet_data = []
        self._initialize()

    def _initialize(self):
        ui = self.ui

    def get_widget(self):
        return self.ui.widget

    def save_input_file(self, solver):
        return solver

    def load_input_file(self, solver):
        pass
