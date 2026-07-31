from pathlib import Path
import shutil

from PySide6.QtWidgets import QMessageBox

from nextlib.utils.ui import load_ui
from view.panel.properties.particle_ui import Ui_ParticleForm


class ParticleData:
    def __init__(self):
        self.name = ''

        self.is_two_dimensional = True
        self.is_domain_general = True

        self.path_field = False
        self.is_manhattan = True
        self.pwb = True
        self.grid = 0

        self.base_dx = 0.5
        self.region_min = [-12, -12, 0]
        self.region_max = [12, 12, 1]

        self.segment_data = []
        # 원본 JSON에서의 particle_generation 배열 인덱스 (binary 항목과 순서를 맞춰 재기록하기 위함).
        # GUI에서 새로 추가된 항목은 None -> 저장 시 맨 뒤로 감.
        self.orig_index = None


class SegmentData:
    def __init__(self):
        self.name = ''
        self.invert_normal = False
        self.mesh_path = ''
        self.material = 'solid'
        self.region_type = 'fixed'
        self.translate = []


class ParticleView:
    def __init__(self, parent):
        self._parent = parent
        self.ui = load_ui(None, Ui_ParticleForm).ui

        self.particle_data = []
        self._binary_passthrough = []
        # 현재 선택된 particle_generation 항목에 속한 모든 segment(벽/field 등)의 미리보기 액터
        self._mesh_preview_actors = []
        # mesh_select로 방금 고른(아직 추가/저장 전인) 파일의 미리보기 액터
        self._mesh_pending_actor = None
        # mesh_select로 방금 고른 파일에 대해 자동 계산한 translate([x,y]).
        # 추가/저장 시 이 값을 세그먼트에 실어 보낸다 (translate 편집 UI가 없어서).
        self._pending_mesh_translate = None

        self._initialize()

    def _initialize(self):
        ui = self.ui

        ui.comboBox_name.currentIndexChanged.connect(self._changed_combo_name)
        ui.pushButton_add.clicked.connect(self._clicked_add)
        ui.pushButton_save.clicked.connect(self._clicked_save)
        ui.pushButton_remove.clicked.connect(self._clicked_remove)

        # .ui 기본값이 비활성(False)인데, particle_generation 항목이 하나라도 있으면
        # 처음부터 세그먼트 이름을 편집할 수 있어야 하므로 항상 켜둔다.
        ui.comboBox_segment_name.setEnabled(True)
        ui.comboBox_segment_name.currentIndexChanged.connect(self._changed_combo_segment_name)
        ui.pushButton_segment_add.clicked.connect(self._clicked_segment_add)
        ui.pushButton_segment_save.clicked.connect(self._clicked_segment_save)
        ui.pushButton_segment_remove.clicked.connect(self._clicked_segment_remove)

        ui.pushButton_mesh_select.clicked.connect(self._clicked_mesh_select)

    def _changed_combo_name(self, index):
        if index == -1:
            return
        self.change_data(index)

    def change_data(self, index):
        ui = self.ui
        index = index if self.particle_data and (0 <= index < len(self.particle_data)) else (
            len(self.particle_data) - 1 if len(self.particle_data) > 0 else -1)

        if index == -1:
            ui.checkBox_two_dimensional.setChecked(False)
            ui.checkBox_domain_general.setChecked(False)
            ui.checkBox_pwb.setChecked(False)

            ui.groupBox_path_field.setChecked(False)
            ui.checkBox_is_manhattan.setChecked(False)

            ui.lineEdit_grid.setText('')

            ui.lineEdit_base_dx.setText('')
            ui.lineEdit_region_min_x.setText('')
            ui.lineEdit_region_min_y.setText('')
            ui.lineEdit_region_max_x.setText('')
            ui.lineEdit_region_max_y.setText('')

            self.change_segment_data(-1)
            self._preview_segments(-1)

        else:
            cur_data = self.particle_data[index]

            ui.checkBox_two_dimensional.setChecked(cur_data.is_two_dimensional)
            ui.checkBox_domain_general.setChecked(cur_data.is_domain_general)
            ui.checkBox_pwb.setChecked(cur_data.pwb)

            ui.groupBox_path_field.setChecked(cur_data.path_field)
            ui.checkBox_is_manhattan.setChecked(cur_data.is_manhattan)

            ui.lineEdit_grid.setText(str(cur_data.grid))

            ui.lineEdit_base_dx.setText(str(cur_data.base_dx))
            ui.lineEdit_region_min_x.setText(str(cur_data.region_min[0]))
            ui.lineEdit_region_min_y.setText(str(cur_data.region_min[1]))
            ui.lineEdit_region_max_x.setText(str(cur_data.region_max[0]))
            ui.lineEdit_region_max_y.setText(str(cur_data.region_max[1]))

            self.change_segment_data(0)
            self._preview_segments(index)

    def _changed_combo_segment_name(self, segment_index):
        self.change_segment_data(segment_index)

    def change_segment_data(self, segment_index):
        ui = self.ui

        particle_index = ui.comboBox_name.currentIndex()
        segment_index = segment_index if self.particle_data[particle_index].segment_data and (0 <= segment_index < len(self.particle_data[particle_index].segment_data)) else (
            len(self.particle_data[particle_index].segment_data) - 1 if len(self.particle_data[particle_index].segment_data) > 0 else -1)

        # segment_data 자체는 change_data()에서 particle 항목 단위로 한꺼번에 미리보기하므로,
        # 여기서는 방금 선택했을 뿐 아직 추가/저장 안 된(pending) 미리보기만 정리한다.
        self._clear_pending_mesh_preview()
        self._pending_mesh_translate = None

        if segment_index == -1:
            ui.checkBox_interval_normal.setChecked(SegmentData().invert_normal)
            ui.lineEdit_segment_mesh_path.setText(SegmentData().mesh_path)
            ui.comboBox_segment_material.setCurrentText(SegmentData().material)
            ui.comboBox_segment_region_type.setCurrentText(SegmentData().region_type)

        else:
            cur_data = self.particle_data[particle_index].segment_data[segment_index]

            ui.checkBox_interval_normal.setChecked(cur_data.invert_normal)
            ui.lineEdit_segment_mesh_path.setText(str(cur_data.mesh_path))
            ui.comboBox_segment_material.setCurrentText(cur_data.material)
            ui.comboBox_segment_region_type.setCurrentText(cur_data.region_type)

    def _clicked_add(self):
        self.add_data()

    def add_data(self):
        ui = self.ui

        name = ui.comboBox_name.currentText()
        if name:
            get_data = self.get_cur_data(ParticleData())

            self.particle_data.append(get_data)
            ui.comboBox_name.addItem(get_data.name)
            ui.comboBox_name.setCurrentIndex(len(self.particle_data) - 1)

    def get_cur_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_name.currentText()
        get_data.is_two_dimensional = ui.checkBox_two_dimensional.isChecked()
        get_data.is_domain_general = ui.checkBox_domain_general.isChecked()
        get_data.pwb = ui.checkBox_pwb.isChecked()

        get_data.path_field = ui.groupBox_path_field.isChecked()
        get_data.is_manhattan = ui.checkBox_is_manhattan.isChecked()

        get_data.grid = ui.lineEdit_grid.text()

        get_data.base_dx = ui.lineEdit_base_dx.text()
        get_data.region_min = [ui.lineEdit_region_min_x.text(), ui.lineEdit_region_min_y.text(), 0]
        get_data.region_max = [ui.lineEdit_region_max_x.text(), ui.lineEdit_region_max_y.text(), 1]

        return get_data

    def _clicked_save(self):
        self.save_data()

    def save_data(self):
        ui = self.ui

        index = ui.comboBox_name.currentIndex()

        cur_data = self.particle_data[index]
        cur_data.name = ui.comboBox_name.currentText()

        self.change_combo_text(ui.comboBox_name, index, cur_data.name)
        self.get_cur_data(cur_data)

    def change_combo_text(self, combo, index, text):
        combo.blockSignals(True)
        combo.removeItem(index)
        combo.insertItem(index, text)
        combo.setCurrentIndex(index)
        combo.blockSignals(False)

    def _clicked_remove(self):
        self.remove_data()

    def remove_data(self):
        ui = self.ui
        index = ui.comboBox_name.currentIndex()
        if index == -1:
            return

        ui.comboBox_name.removeItem(index)
        del self.particle_data[index]

        self.change_data(index)

    def _clicked_segment_add(self):
        particle_index = self.ui.comboBox_name.currentIndex()
        self.add_segment_data(particle_index)

    def add_segment_data(self, index):
        ui = self.ui

        name = ui.comboBox_segment_name.currentText()
        if name:
            get_data = self.get_cur_segment_data(SegmentData())

            self.particle_data[index].segment_data.append(get_data)
            ui.comboBox_segment_name.addItem(get_data.name)
            ui.comboBox_segment_name.setCurrentIndex(len(self.particle_data[index].segment_data) - 1)
            self._preview_segments(index)

    def get_cur_segment_data(self, get_data=None):
        ui = self.ui

        get_data.name = ui.comboBox_segment_name.currentText()
        get_data.invert_normal = ui.checkBox_interval_normal.isChecked()

        get_data.mesh_path = ui.lineEdit_segment_mesh_path.text()
        get_data.material = ui.comboBox_segment_material.currentText()
        get_data.region_type = ui.comboBox_segment_region_type.currentText()

        # mesh_select로 방금 새 파일을 골랐을 때만 자동 계산된 translate를 반영한다.
        # (translate 편집 UI가 없어서, 기존 항목을 그냥 저장할 때는 원래 값을 그대로 둔다)
        if self._pending_mesh_translate is not None:
            get_data.translate = list(self._pending_mesh_translate)
            self._pending_mesh_translate = None

        return get_data

    def _clicked_segment_save(self):
        self.save_segment_data()

    def save_segment_data(self):
        ui = self.ui

        particle_index = ui.comboBox_name.currentIndex()
        segment_index = ui.comboBox_segment_name.currentIndex()

        cur_data = self.particle_data[particle_index].segment_data[segment_index]
        cur_data.name = ui.comboBox_segment_name.currentText()

        self.change_segment_combo_text(ui.comboBox_segment_name, segment_index, cur_data.name)
        self.get_cur_segment_data(cur_data)
        self._preview_segments(particle_index)

    def change_segment_combo_text(self, combo, index, text):
        combo.blockSignals(True)
        combo.removeItem(index)
        combo.insertItem(index, text)
        combo.setCurrentIndex(index)
        combo.blockSignals(False)

    def _clicked_segment_remove(self):
        self.remove_segment_data()

    def remove_segment_data(self):
        ui = self.ui
        particle_index = ui.comboBox_name.currentIndex()
        segment_index = ui.comboBox_segment_name.currentIndex()
        if segment_index == -1:
            return

        ui.comboBox_segment_name.removeItem(segment_index)
        if segment_index < len(self.particle_data[particle_index].segment_data):
            del self.particle_data[particle_index].segment_data[segment_index]
            self.change_segment_data(segment_index)
            self._preview_segments(particle_index)

    def load_input_file(self, solver):
        ui = self.ui
        particles = solver.data.get('config.particle_generation')
        if not particles:
            return

        ui.comboBox_name.blockSignals(True)
        self.particle_data.clear()
        self._binary_passthrough.clear()
        ui.comboBox_name.clear()

        for i, p in enumerate(particles):
            if 'binary_path' in p:
                # GUI에서 편집 불가한 초기 군중 binary 항목은 원본 그대로 보존 (원본 순서도 함께 기록)
                self._binary_passthrough.append((i, dict(p)))
                continue

            d = ParticleData()
            d.orig_index = i
            d.name = f'gen_{i}'
            d.is_two_dimensional = bool(p.get('two_dimensional', True))
            d.is_domain_general = bool(p.get('domain_general', True))
            d.path_field = bool(p.get('path_field', False))
            d.is_manhattan = bool(p.get('is_manhattan', False))
            d.pwb = bool(p.get('pwb', False))
            d.grid = str(p.get('grid', 0))
            d.base_dx = str(p.get('base_dx', 0.4))

            base_region = p.get('base_region', {})
            mn = base_region.get('min', [-12, -12, 0])
            mx = base_region.get('max', [12, 12, 1])
            d.region_min = [str(mn[0]), str(mn[1]), str(mn[2]) if len(mn) > 2 else '0']
            d.region_max = [str(mx[0]), str(mx[1]), str(mx[2]) if len(mx) > 2 else '1']

            for seg in p.get('regional_segment', []):
                s = SegmentData()
                s.name = str(seg.get('name', ''))
                s.mesh_path = str(seg.get('mesh_path', ''))
                s.invert_normal = bool(seg.get('invert_normal', False))
                s.material = str(seg.get('material', 'solid'))
                s.region_type = str(seg.get('region_type', 'fixed'))
                s.translate = seg.get('translate', [])
                d.segment_data.append(s)

            self.particle_data.append(d)
            ui.comboBox_name.addItem(d.name)

        ui.comboBox_name.blockSignals(False)

        if self.particle_data:
            ui.comboBox_name.setCurrentIndex(0)
            self.change_data(0)
            # populate segment combo for first particle
            ui.comboBox_segment_name.blockSignals(True)
            ui.comboBox_segment_name.clear()
            for s in self.particle_data[0].segment_data:
                ui.comboBox_segment_name.addItem(s.name)
            ui.comboBox_segment_name.blockSignals(False)
            if self.particle_data[0].segment_data:
                ui.comboBox_segment_name.setCurrentIndex(0)
                self.change_segment_data(0)

    def _clicked_mesh_select(self):
        from nextlib.dialogbox.dialogbox import FileDialogBox

        filters = 'stl (*.stl);;All file (*.*)'
        get_file = FileDialogBox.open_file(self._parent, filters=filters)
        if not get_file:
            return

        src = Path(get_file)
        project_path = getattr(getattr(self._parent, 'prj', None), 'path', None)
        if not project_path:
            self._apply_mesh_selection(str(src))
            return

        stl_dir = Path(project_path) / 'stl'
        dest = stl_dir / src.name

        if dest.exists() and dest.resolve() != src.resolve():
            box = QMessageBox(self._parent)
            box.setWindowTitle('파일 이름 중복')
            box.setText(f"stl 폴더에 이미 '{src.name}' 파일이 있습니다.\n어떻게 하시겠습니까?")
            overwrite_btn = box.addButton('덮어쓰기', QMessageBox.ButtonRole.AcceptRole)
            keep_btn = box.addButton('복사 안하고 기존 폴더 사용', QMessageBox.ButtonRole.DestructiveRole)
            cancel_btn = box.addButton('취소', QMessageBox.ButtonRole.RejectRole)
            box.setDefaultButton(cancel_btn)
            box.exec()
            clicked = box.clickedButton()

            if clicked == cancel_btn:
                return
            if clicked == keep_btn:
                # 새로 고른 파일은 복사하지 않고, stl 폴더에 이미 있던 파일을 그대로 쓴다.
                self._apply_mesh_selection(f'stl/{dest.name}')
                return
            # overwrite_btn -> 아래에서 복사 진행

        stl_dir.mkdir(parents=True, exist_ok=True)
        if dest.resolve() != src.resolve():
            shutil.copy2(src, dest)

        self._apply_mesh_selection(f'stl/{dest.name}')

    def _apply_mesh_selection(self, rel_or_abs_path):
        self.ui.lineEdit_segment_mesh_path.setText(rel_or_abs_path)
        # translate를 편집하는 UI가 없으므로, 방금 고른 STL의 원본 좌표 중심이 도메인
        # 중심에 오도록 translate를 자동 계산해서 채워둔다 (안 그러면 STL의 실측
        # 좌표(수십만 단위)가 그대로 남아 도메인/지도와 동떨어진 곳에 위치하게 된다).
        self._pending_mesh_translate = self._compute_auto_translate(rel_or_abs_path)
        self._preview_pending_mesh(rel_or_abs_path)

    def _compute_auto_translate(self, mesh_path):
        get_domain = getattr(self._parent, '_get_domain', None)
        if get_domain is None:
            return None
        d_min, d_max = get_domain()
        if d_min is None or d_max is None:
            return None

        resolved = self._resolve_mesh_path(mesh_path)
        if not resolved.is_file():
            return None

        import vtk
        reader = vtk.vtkSTLReader()
        reader.SetFileName(str(resolved))
        reader.Update()
        bounds = reader.GetOutput().GetBounds()
        if any(b != b for b in bounds):  # NaN 체크 (빈 폴리데이터 등)
            return None

        stl_cx = (bounds[0] + bounds[1]) / 2.0
        stl_cy = (bounds[2] + bounds[3]) / 2.0
        dom_cx = (d_min[0] + d_max[0]) / 2.0
        dom_cy = (d_min[1] + d_max[1]) / 2.0
        return [dom_cx - stl_cx, dom_cy - stl_cy]

    def _resolve_mesh_path(self, mesh_path):
        path = Path(mesh_path)
        if path.is_absolute():
            return path
        project_path = getattr(getattr(self._parent, 'prj', None), 'path', None)
        if project_path:
            return Path(project_path) / path
        return path

    def _load_mesh_actor(self, mesh_path, translate=None):
        vtk = getattr(self._parent, 'vtk', None)
        if vtk is None or not mesh_path:
            return None

        resolved = self._resolve_mesh_path(mesh_path)
        if not resolved.is_file():
            return None

        from nextlib.vtk.core.mesh_loader import MeshLoader
        actor = MeshLoader().load_stl(resolved)
        if actor is None:
            return None

        actor.GetProperty().SetOpacity(0.5)
        # 솔버는 mesh_path의 STL 원본 좌표에 translate를 더해서 도메인 안으로 옮겨 배치하므로
        # (원본 STL이 실측 좌표계 등 큰 좌표를 쓰는 경우가 많음), 미리보기도 똑같이 옮겨야
        # 배경 지도/도메인과 위치가 맞는다. 안 옮기면 화면 밖 먼 곳에 그려져 사실상 안 보인다.
        if translate:
            tx = float(translate[0]) if len(translate) > 0 else 0.0
            ty = float(translate[1]) if len(translate) > 1 else 0.0
            tz = float(translate[2]) if len(translate) > 2 else 0.0
            actor.SetPosition(tx, ty, tz)

        # translate가 아직 없는(새로 추가했거나 저장 전인) 세그먼트는 원본 STL의 실측
        # 좌표(수십만 단위)에 그대로 남아있을 수 있다. 이런 액터가 카메라 fit/reset
        # 계산에 끼면 도메인/지도가 점처럼 작아져 사실상 안 보이게 되므로, 미리보기
        # 액터는 (위치가 맞든 안 맞든) 항상 카메라 bounds 계산에서 제외한다.
        actor.SetUseBounds(False)
        return actor

    def _preview_segments(self, particle_index):
        """현재 선택된 particle_generation 항목에 속한 모든 segment(벽/field 등) 형상을
        한꺼번에 뷰포트에 미리보기 (segment 콤보를 옮겨도 이전에 추가된 형상이 안 사라지게)"""
        vtk = getattr(self._parent, 'vtk', None)
        for actor in self._mesh_preview_actors:
            if vtk is not None:
                vtk.renderer.RemoveActor(actor)
        self._mesh_preview_actors = []

        if vtk is not None and 0 <= particle_index < len(self.particle_data):
            for seg in self.particle_data[particle_index].segment_data:
                actor = self._load_mesh_actor(seg.mesh_path, seg.translate)
                if actor is not None:
                    vtk.renderer.AddActor(actor)
                    self._mesh_preview_actors.append(actor)

        if vtk is not None:
            vtk.vtk_widget.GetRenderWindow().Render()

    def _preview_pending_mesh(self, mesh_path):
        """mesh_select로 방금 고른(아직 추가/저장 전인) 파일을 추가로 미리보기"""
        self._clear_pending_mesh_preview()
        vtk = getattr(self._parent, 'vtk', None)
        actor = self._load_mesh_actor(mesh_path, self._pending_mesh_translate)
        if vtk is None or actor is None:
            return

        vtk.renderer.AddActor(actor)
        self._mesh_pending_actor = actor
        vtk.vtk_widget.GetRenderWindow().Render()

    def _clear_pending_mesh_preview(self):
        vtk = getattr(self._parent, 'vtk', None)
        if vtk is not None and self._mesh_pending_actor is not None:
            vtk.renderer.RemoveActor(self._mesh_pending_actor)
            vtk.vtk_widget.GetRenderWindow().Render()
        self._mesh_pending_actor = None

    def _clear_mesh_preview(self):
        """프로젝트를 새로 열 때 등, 미리보기 전체를 정리"""
        vtk = getattr(self._parent, 'vtk', None)
        for actor in self._mesh_preview_actors:
            if vtk is not None:
                vtk.renderer.RemoveActor(actor)
        self._mesh_preview_actors = []
        self._clear_pending_mesh_preview()

    def get_widget(self):
        return self.ui.widget

    def save_input_file(self, solver):
        # binary(passthrough)/domain_general 항목을 원본 particle_generation 배열의 순서 그대로
        # 다시 섞어 써야 한다 (그렇지 않으면 항목 자체는 안 잃어버려도 순서가 뒤바뀜).
        # orig_index가 없는(= GUI에서 새로 추가된) 항목은 원본에 없던 것이므로 맨 뒤로 보낸다.
        entries = [(orig_index, 'binary', raw) for orig_index, raw in self._binary_passthrough]
        entries += [(d.orig_index, 'domain', d) for d in self.particle_data]
        entries.sort(key=lambda e: (e[0] is None, e[0] if e[0] is not None else 0))

        for _, kind, payload in entries:
            if kind == 'binary':
                solver.data.add('config.particle_generation', dict(payload))
                continue

            d = payload
            idx = len(solver.data.get('config.particle_generation') or [])
            solver.add_particle_generation(int(d.grid))

            solver.data.set(f'config.particle_generation[{idx}].two_dimensional', d.is_two_dimensional)
            solver.data.set(f'config.particle_generation[{idx}].domain_general', d.is_domain_general)
            solver.data.set(f'config.particle_generation[{idx}].pwb', d.pwb)

            if d.path_field:
                solver.data.set(f'config.particle_generation[{idx}].path_field', d.path_field)
                solver.data.set(f'config.particle_generation[{idx}].is_manhattan', d.is_manhattan)

            solver.data.set(f'config.particle_generation[{idx}].base_dx', float(d.base_dx))
            solver.data.set(f'config.particle_generation[{idx}].base_region.min[0]', float(d.region_min[0]))
            solver.data.set(f'config.particle_generation[{idx}].base_region.min[1]', float(d.region_min[1]))
            solver.data.set(f'config.particle_generation[{idx}].base_region.min[2]', float(d.region_min[2]))
            solver.data.set(f'config.particle_generation[{idx}].base_region.max[0]', float(d.region_max[0]))
            solver.data.set(f'config.particle_generation[{idx}].base_region.max[1]', float(d.region_max[1]))
            solver.data.set(f'config.particle_generation[{idx}].base_region.max[2]', float(d.region_max[2]))

            for j, e in enumerate(d.segment_data):
                solver.add_particle_generation_regional_segment(idx, e.name, e.mesh_path, e.invert_normal, e.material, e.region_type)
                if getattr(e, 'translate', []):
                    solver.data.set(f'config.particle_generation[{idx}].regional_segment[{j}].translate', e.translate)

            solver.data.set(f'config.particle_generation[{idx}].grid', int(d.grid))

        return solver

