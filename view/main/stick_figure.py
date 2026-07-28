"""솔버 결과 VTK 파일을 3D 스틱피겨(사람 모형) vtkAssembly로 변환

바이너리 legacy VTK 파일에서 입자 위치/속도를 읽어:
- 밀집도(spatial hash) 기반 컬러맵 (녹색 → 파랑 → 노랑 → 주황 → 빨강)
- velocity 방향 회전 + step 기반 걷기 모션
을 적용한 스틱피겨 assembly를 만든다.

프레임당 입자 수가 수만 개 수준이라 순수 파이썬 반복문으로는 느려서,
전 구간을 numpy 배열 연산으로 처리한다 (밀집도는 scipy KD-tree로 이웃 검색).
"""
import math
import re
import struct
from pathlib import Path

import numpy as np
import vtk
from scipy.spatial import cKDTree
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

# 스틱피겨 치수
H = 2.0          # 키
TUBE_R = 0.06    # 팔다리 튜브 반경
HEAD_R = 0.18    # 머리 반경

# 밀집도 계산 반경 (m)
DENSITY_RADIUS = 3.0

# 밀집도 컬러맵: (위치 0~1, RGB)
COLOR_STOPS = [
    (0.00, (0, 255, 0)),    # 녹색 (밀집도 최저)
    (0.25, (0, 0, 255)),    # 파랑
    (0.50, (255, 255, 0)),  # 노랑
    (0.75, (255, 165, 0)),  # 주황
    (1.00, (255, 0, 0)),    # 빨강 (밀집도 최고)
]

_FIELD_TYPE_SIZES = {'unsigned_char': 1, 'float': 4, 'int': 4}


def _read_points(filepath):
    """바이너리 legacy VTK에서 (positions (N,2) float64 배열, rest_bytes) 반환. 실패 시 (None, None)"""
    with open(filepath, 'rb') as f:
        # POINTS 라인을 찾을 때까지 헤더 스캔 (고정 줄 수 가정 제거)
        points_line = None
        for _ in range(20):
            line = f.readline()
            if not line:
                break
            text = line.decode('ascii', errors='replace').strip()
            if text.upper().startswith('POINTS'):
                points_line = text
                break
        if points_line is None:
            return None, None

        try:
            num_points = int(points_line.split()[1])
        except (IndexError, ValueError):
            return None, None

        points_data = f.read(num_points * 3 * 4)
        rest_bytes = f.read()

    if num_points == 0 or len(points_data) < num_points * 3 * 4:
        return None, None

    # legacy VTK 바이너리는 big-endian
    arr = np.frombuffer(points_data, dtype='>f4').reshape(num_points, 3)
    positions = arr[:, :2].astype(np.float64)
    return positions, rest_bytes


def _read_velocities(rest_bytes, num_points):
    """FIELD 섹션에서 velocity 배열을 읽는다 (N,2) float64. 없으면 0 벡터"""
    velocities = np.zeros((num_points, 2), dtype=np.float64)
    try:
        header_text = rest_bytes.decode('ascii', errors='replace')
        field_match = re.search(r'FIELD\s+\S+\s+(\d+)', header_text)
        if not field_match:
            return velocities

        num_fields = int(field_match.group(1))
        cursor = header_text.index('\n', field_match.start()) + 1

        for _ in range(num_fields):
            nl = header_text.index('\n', cursor)
            field_line = header_text[cursor:nl].strip()
            cursor = nl + 1
            parts = field_line.split()
            if len(parts) < 4:
                continue
            fname, ncomp, ntuples, dtype = parts[0], int(parts[1]), int(parts[2]), parts[3]
            data_size = ncomp * ntuples * _FIELD_TYPE_SIZES.get(dtype, 4)

            if fname == 'velocity' and ncomp >= 2:
                vel_bytes = rest_bytes[cursor:cursor + data_size]
                vel_arr = np.frombuffer(vel_bytes, dtype='>f4').reshape(ntuples, ncomp)
                velocities = vel_arr[:, :2].astype(np.float64)

            cursor += data_size
            while cursor < len(header_text) and header_text[cursor] == '\n':
                cursor += 1
    except Exception:
        pass
    return velocities


def _compute_densities(positions):
    """positions (N,2) 배열 -> (valid 불리언 배열, densities 배열, max_density). KD-tree로 반경 내 이웃 수 계산"""
    n = positions.shape[0]
    valid = np.isfinite(positions).all(axis=1)
    densities = np.zeros(n, dtype=np.float64)

    valid_idx = np.flatnonzero(valid)
    if valid_idx.size == 0:
        return valid, densities, 1.0

    pts = positions[valid_idx]
    tree = cKDTree(pts)
    # query_ball_point가 자기 자신도 포함해서 세므로 1을 빼 "이웃 수"로 맞춤 (기존 로직과 동일)
    counts = tree.query_ball_point(pts, r=DENSITY_RADIUS, return_length=True) - 1
    densities[valid_idx] = counts.astype(np.float64)

    max_density = float(counts.max()) if counts.size else 1.0
    return valid, densities, max(max_density, 1.0)


def _build_lut(max_density):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(256)
    lut.SetRange(0.0, max_density)
    lut.SetIndexedLookup(False)
    for idx in range(256):
        t = idx / 255.0
        for k in range(len(COLOR_STOPS) - 1):
            t0, c0 = COLOR_STOPS[k]
            t1, c1 = COLOR_STOPS[k + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
                r = (c0[0] + (c1[0] - c0[0]) * f) / 255.0
                g = (c0[1] + (c1[1] - c0[1]) * f) / 255.0
                b = (c0[2] + (c1[2] - c0[2]) * f) / 255.0
                lut.SetTableValue(idx, r, g, b, 1.0)
                break
    lut.Build()
    return lut


def _lines_polydata_from_segments(starts, ends, scalars):
    """starts/ends: (M,3) float 배열, scalars: (M,) 또는 None. 세그먼트별 line cell을 가진 vtkPolyData 생성"""
    m = starts.shape[0]
    poly = vtk.vtkPolyData()
    if m == 0:
        return poly

    pts = np.empty((2 * m, 3), dtype=np.float64)
    pts[0::2] = starts
    pts[1::2] = ends

    vtk_points = vtk.vtkPoints()
    vtk_points.SetData(numpy_to_vtk(pts, deep=True))
    poly.SetPoints(vtk_points)

    conn = np.empty((m, 3), dtype=np.int64)
    conn[:, 0] = 2
    conn[:, 1] = np.arange(0, 2 * m, 2)
    conn[:, 2] = np.arange(1, 2 * m, 2)
    cells = vtk.vtkCellArray()
    cells.SetCells(m, numpy_to_vtkIdTypeArray(conn.ravel(), deep=True))
    poly.SetLines(cells)

    if scalars is not None:
        dup = np.empty(2 * m, dtype=np.float32)
        dup[0::2] = scalars
        dup[1::2] = scalars
        scalars_vtk = numpy_to_vtk(dup, deep=True)
        scalars_vtk.SetName('density')
        poly.GetPointData().SetScalars(scalars_vtk)

    return poly


def load_stick_figure(filepath):
    """VTK 파일 로드 → 3D 스틱피겨 vtkAssembly (실패 시 None)"""
    if not Path(filepath).exists():
        return None

    step_match = re.search(r'_(\d+)\.vtk$', str(filepath))
    step_num = int(step_match.group(1)) if step_match else 0

    positions, rest_bytes = _read_points(filepath)
    if positions is None:
        return None
    num_points = positions.shape[0]

    valid, densities, max_density = _compute_densities(positions)
    velocities = _read_velocities(rest_bytes, num_points)

    idx = np.flatnonzero(valid)
    n = idx.size

    px = positions[idx, 0]
    py = positions[idx, 1]
    vx = velocities[idx, 0]
    vy = velocities[idx, 1]
    density_val = densities[idx].astype(np.float32)

    speed = np.hypot(vx, vy)
    angle = np.where(speed > 0.01, np.arctan2(vy, vx) - math.pi / 2, 0.0)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    def w(lx, ly, lz):
        """로컬(스칼라/배열)→월드 좌표 (n,3) 배열: XY를 angle만큼 회전, Z는 높이"""
        wx = lx * cos_a - ly * sin_a + px
        wy = lx * sin_a + ly * cos_a + py
        wz = np.broadcast_to(np.asarray(lz, dtype=np.float64), wx.shape)
        return np.stack([wx, wy, wz], axis=1)

    # 원본 코드는 (invalid 포인트를 건너뛰기 전) 원본 배열 인덱스를 phase 계산에 쓰므로
    # 압축된 순번(np.arange(n))이 아니라 idx(원본 인덱스)를 그대로 써야 동일한 결과가 나온다.
    phase = step_num * 0.5 + idx.astype(np.float64) * 1.7
    swing = np.sin(phase) * 0.35
    arm_swing = -swing

    feet_z = 0.0
    hip_z = H * 0.45
    neck_z = H * 0.78
    head_z = H * 0.90

    hip = w(0.0, 0.0, hip_z)
    neck = w(0.0, 0.0, neck_z)

    l_foot = w(-H * 0.1, swing * H * 0.25, feet_z)
    r_foot = w(H * 0.1, -swing * H * 0.25, feet_z)
    l_knee = w(-H * 0.08, swing * H * 0.1, hip_z * 0.5)
    r_knee = w(H * 0.08, -swing * H * 0.1, hip_z * 0.5)

    l_shoulder = w(-H * 0.15, 0.0, neck_z)
    r_shoulder = w(H * 0.15, 0.0, neck_z)
    l_hand = w(-H * 0.18, arm_swing * H * 0.25, H * 0.50)
    r_hand = w(H * 0.18, -arm_swing * H * 0.25, H * 0.50)

    head_center = w(0.0, 0.0, head_z)

    # 몸통/팔다리 8개 세그먼트를 particle 전체에 대해 한 번에 이어붙임
    body_starts = np.concatenate(
        [hip, l_shoulder, hip, l_knee, hip, r_knee, l_shoulder, r_shoulder], axis=0)
    body_ends = np.concatenate(
        [neck, r_shoulder, l_knee, l_foot, r_knee, r_foot, l_hand, r_hand], axis=0)
    body_scalars = np.tile(density_val, 8)

    line_poly = _lines_polydata_from_segments(body_starts, body_ends, body_scalars)

    tube = vtk.vtkTubeFilter()
    tube.SetInputData(line_poly)
    tube.SetRadius(TUBE_R)
    tube.SetNumberOfSides(6)
    tube.CappingOn()
    tube.Update()

    lut = _build_lut(max_density)

    body_mapper = vtk.vtkPolyDataMapper()
    body_mapper.SetInputConnection(tube.GetOutputPort())
    body_mapper.SetScalarModeToUsePointData()
    body_mapper.SetLookupTable(lut)
    body_mapper.SetScalarRange(0.0, max_density)

    body_actor = vtk.vtkActor()
    body_actor.SetMapper(body_mapper)

    # 머리 (입자당 점 하나 + 구 글리프)
    head_poly = vtk.vtkPolyData()
    head_points = vtk.vtkPoints()
    head_points.SetData(numpy_to_vtk(head_center, deep=True))
    head_poly.SetPoints(head_points)
    head_scalars_vtk = numpy_to_vtk(density_val, deep=True)
    head_scalars_vtk.SetName('density')
    head_poly.GetPointData().SetScalars(head_scalars_vtk)

    sphere_src = vtk.vtkSphereSource()
    sphere_src.SetRadius(HEAD_R)
    sphere_src.SetPhiResolution(10)
    sphere_src.SetThetaResolution(10)

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(head_poly)
    glyph.SetSourceConnection(sphere_src.GetOutputPort())
    glyph.SetScaleModeToDataScalingOff()
    glyph.Update()

    head_mapper = vtk.vtkPolyDataMapper()
    head_mapper.SetInputConnection(glyph.GetOutputPort())
    head_mapper.SetScalarModeToUsePointData()
    head_mapper.SetLookupTable(lut)
    head_mapper.SetScalarRange(0.0, max_density)

    head_actor = vtk.vtkActor()
    head_actor.SetMapper(head_mapper)

    # 그림자 (바닥에 깔리는 8개 세그먼트, 색상 없음)
    shadow_z = np.zeros(n, dtype=np.float64) + 0.001
    body_parts = [hip, neck, l_shoulder, r_shoulder, l_knee, r_knee, l_foot, r_foot, l_hand, r_hand]
    shadow_parts = [np.stack([p[:, 0], p[:, 1], shadow_z], axis=1) for p in body_parts]
    shadow_segs = [(0, 1), (2, 3), (0, 4), (4, 6), (0, 5), (5, 7), (2, 8), (3, 9)]

    shadow_starts = np.concatenate([shadow_parts[s1] for s1, s2 in shadow_segs], axis=0)
    shadow_ends = np.concatenate([shadow_parts[s2] for s1, s2 in shadow_segs], axis=0)

    shadow_poly = _lines_polydata_from_segments(shadow_starts, shadow_ends, None)

    shadow_tube = vtk.vtkTubeFilter()
    shadow_tube.SetInputData(shadow_poly)
    shadow_tube.SetRadius(TUBE_R * 1.5)
    shadow_tube.SetNumberOfSides(4)
    shadow_tube.CappingOn()
    shadow_tube.Update()

    shadow_mapper = vtk.vtkPolyDataMapper()
    shadow_mapper.SetInputConnection(shadow_tube.GetOutputPort())
    shadow_mapper.ScalarVisibilityOff()

    shadow_actor = vtk.vtkActor()
    shadow_actor.SetMapper(shadow_mapper)
    shadow_actor.GetProperty().SetColor(0, 0, 0)
    shadow_actor.GetProperty().SetOpacity(0.3)

    assembly = vtk.vtkAssembly()
    assembly.AddPart(shadow_actor)
    assembly.AddPart(body_actor)
    assembly.AddPart(head_actor)

    return assembly
