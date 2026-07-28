"""배경 지도 이미지를 VTK 렌더러에 로드

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.vtk, self.prj, self.prop_grid
"""
import shutil
from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from datarw.e8ight.solver_input import SolverData


class BackgroundMapMixin:
    """케이스 map/ 폴더의 지도 이미지를 도메인 좌표에 맞춰 표시"""

    def _select_background_map(self):
        """사용자가 배경 이미지를 선택하여 케이스 map/ 폴더에 복사 후 로드"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, '배경 지도 이미지 선택', '',
            '이미지 파일 (*.jpg *.jpeg *.png *.bmp);;All Files (*)')
        if not filepath:
            return
        # 케이스 map/ 폴더에 복사
        if self.prj.path:
            map_dir = Path(self.prj.path) / 'map'
            map_dir.mkdir(parents=True, exist_ok=True)
            dest = map_dir / Path(filepath).name
            if str(Path(filepath).resolve()) != str(dest.resolve()):
                shutil.copy2(filepath, dest)
            self._bg_map_path = str(dest)
        else:
            self._bg_map_path = filepath
        self._load_background_map(self._bg_map_path)

    def _find_map_file(self):
        """표시할 지도 이미지 경로 탐색 (케이스 map/ → resource/map 순)"""
        if getattr(self, '_bg_map_path', None):
            return Path(self._bg_map_path)

        if self.prj.path:
            case_map_dir = Path(self.prj.path) / 'map'
            if case_map_dir.is_dir():
                for ext in ('*.jpg', '*.jpeg', '*.png', '*.bmp'):
                    files = list(case_map_dir.glob(ext))
                    if files:
                        return files[0]

        res_map_dir = Path(__file__).resolve().parent.parent.parent / 'resource' / 'map'
        for ext in ('*.jpg', '*.jpeg', '*.png'):
            files = list(res_map_dir.glob(ext))
            if files:
                return files[0]
        return None

    def _get_domain(self):
        """배경을 깔 도메인 XY 범위: Grid 패널 → JSON 순으로 조회"""
        if hasattr(self, 'prop_grid') and self.prop_grid.grid_data:
            gd = self.prop_grid.grid_data[0]
            try:
                d_min = [float(gd.domain_min[0]), float(gd.domain_min[1])]
                d_max = [float(gd.domain_max[0]), float(gd.domain_max[1])]
                return d_min, d_max
            except (ValueError, IndexError):
                pass

        json_path = Path(rf'{self.prj.path}/{self.prj.name}.json')
        if not json_path.is_file():
            return None, None
        solver = SolverData()
        solver.load(json_path)
        grids = solver.data.get('config.grid')
        if not grids or len(grids) == 0:
            return None, None
        domain = grids[0].get('domain', {})
        d_min = domain.get('min', [-155, -125, 1])[:2]
        d_max = domain.get('max', [210, 165, 1])[:2]
        return d_min, d_max

    def _remove_background_actors(self):
        if getattr(self, '_bg_map_actor', None) is not None:
            self.vtk.renderer.RemoveActor(self._bg_map_actor)
            self._bg_map_actor = None
        if getattr(self, '_bg_overlay_actor', None) is not None:
            self.vtk.renderer.RemoveActor(self._bg_overlay_actor)
            self._bg_overlay_actor = None

    def _load_background_map(self, image_path=None):
        """배경 지도 이미지를 VTK 렌더러에 로드"""
        import vtk

        if image_path:
            map_file = Path(image_path)
        else:
            map_file = self._find_map_file()

        if map_file is None or not Path(map_file).exists():
            return

        d_min, d_max = self._get_domain()
        if d_min is None or d_max is None:
            return

        suffix = Path(map_file).suffix.lower()
        if suffix in ('.jpg', '.jpeg'):
            reader = vtk.vtkJPEGReader()
        elif suffix == '.bmp':
            reader = vtk.vtkBMPReader()
        else:
            reader = vtk.vtkPNGReader()
        reader.SetFileName(str(map_file))
        reader.Update()

        plane = vtk.vtkPlaneSource()
        plane.SetOrigin(d_min[0], d_min[1], -0.01)
        plane.SetPoint1(d_max[0], d_min[1], -0.01)
        plane.SetPoint2(d_min[0], d_max[1], -0.01)
        plane.Update()

        texture = vtk.vtkTexture()
        texture.SetInputConnection(reader.GetOutputPort())
        texture.InterpolateOn()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetTexture(texture)

        # 지도 위 반투명 어두운 오버레이 (입자 대비 강화)
        overlay_plane = vtk.vtkPlaneSource()
        overlay_plane.SetOrigin(d_min[0], d_min[1], -0.005)
        overlay_plane.SetPoint1(d_max[0], d_min[1], -0.005)
        overlay_plane.SetPoint2(d_min[0], d_max[1], -0.005)
        overlay_plane.Update()

        overlay_mapper = vtk.vtkPolyDataMapper()
        overlay_mapper.SetInputConnection(overlay_plane.GetOutputPort())

        overlay_actor = vtk.vtkActor()
        overlay_actor.SetMapper(overlay_mapper)
        overlay_actor.GetProperty().SetColor(0, 0, 0)
        overlay_actor.GetProperty().SetOpacity(getattr(self, '_bg_dim_level', 0.4))

        self._remove_background_actors()

        self._bg_map_actor = actor
        self._bg_overlay_actor = overlay_actor
        self.vtk.renderer.AddActor(actor)
        self.vtk.renderer.AddActor(overlay_actor)
        self.vtk.renderer.ResetCamera()
        self.vtk.vtk_widget.GetRenderWindow().Render()
