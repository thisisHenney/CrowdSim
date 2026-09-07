from nextlib.utils.ui import load_ui
from view.panel.properties.grid_ui import Ui_GridForm
from view.panel.properties import _extra_ui


_KNOWN_GRID_KEYS = {'name', 'domain', 'width', 'max_particle'}


_EDIT_FIELDS = (
    'lineEdit_min_x',
    'lineEdit_min_y',
    'lineEdit_max_x',
    'lineEdit_max_y',
    'lineEdit_width',
    'lineEdit_max_particle',
    # 항목이 없으면 저장/삭제도 대상이 없다.
    # ('추가'는 잠그지 않는다 - 첫 항목을 만드는 유일한 길이다)
    'pushButton_save',
    'pushButton_remove',
)


class GridData:
    def __init__(self):
        self.name = ''

        self.domain_min = [-1, -1]
        self.domain_max = [1, 1]
        self.width = -1
        self.max_particle = 10000
        self.raw_extra = {}


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
        if not (0 <= index < len(self.grid_data)):
            return
        self.get_cur_data(self.grid_data[index])
        parent = getattr(self, '_parent', None)
        if parent is not None and hasattr(parent, 'set_dirty'):
            parent.set_dirty(True)

    def change_data(self, index):
        self._filling = True
        try:
            ui = self.ui

            index = index if self.grid_data and (0 <= index < len(self.grid_data)) else (
                len(self.grid_data) - 1 if len(self.grid_data) > 0 else -1)

            if index == -1:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, False)
                ui.lineEdit_min_x.setText('')
                ui.lineEdit_min_y.setText('')
                ui.lineEdit_max_x.setText('')
                ui.lineEdit_max_y.setText('')

                ui.lineEdit_width.setText('')
                ui.lineEdit_max_particle.setText('')

            else:
                _extra_ui.set_fields_enabled(ui, _EDIT_FIELDS, True)
                cur_data = self.grid_data[index]

                ui.lineEdit_min_x.setText(str(cur_data.domain_min[0]))
                ui.lineEdit_min_y.setText(str(cur_data.domain_min[1]))
                ui.lineEdit_max_x.setText(str(cur_data.domain_max[0]))
                ui.lineEdit_max_y.setText(str(cur_data.domain_max[1]))

                ui.lineEdit_width.setText(str(cur_data.width))
                ui.lineEdit_max_particle.setText(str(cur_data.max_particle))
        finally:
            self._filling = False

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

        # Grid는 도메인 정의라 삭제해도 다른 패널의 grid 인덱스를
        # 자동으로 당기지 않는다. 아래처럼 재정렬하면 inlet/outlet의
        # grid 참조가 어긋나므로 의도적으로 두지 않는다.
        #
        # for panel in (self._parent.prop_inlet, self._parent.prop_outlet):
        #     for d in panel.data:
        #         if int(d.grid) > index:
        #             d.grid = int(d.grid) - 1
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

            for k, v in getattr(d, 'raw_extra', {}).items():
                solver.data.set(f'config.grid[{i}].{k}', v)

        return solver

    def load_input_file(self, solver):
        ui = self.ui
        grids = solver.data.get('config.grid')
        if not grids:
            # 섹션이 비어 있으면 이전 프로젝트 값이 남지 않도록 비운다
            ui.comboBox_name.blockSignals(True)
            self.grid_data.clear()
            ui.comboBox_name.clear()
            ui.comboBox_name.blockSignals(False)
            self.change_data(-1)
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
            d.raw_extra = {k: v for k, v in g.items() if k not in _KNOWN_GRID_KEYS}
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
