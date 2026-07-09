"""솔버 결과 VTK 파일을 3D 스틱피겨(사람 모형) vtkAssembly로 변환

바이너리 legacy VTK 파일에서 입자 위치/속도를 읽어:
- 밀집도(spatial hash) 기반 컬러맵 (녹색 → 파랑 → 노랑 → 주황 → 빨강)
- velocity 방향 회전 + step 기반 걷기 모션
을 적용한 스틱피겨 assembly를 만든다.
"""
import math
import re
import struct
from pathlib import Path

import vtk

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
    """바이너리 legacy VTK에서 (positions, rest_bytes) 반환. 실패 시 (None, None)"""
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

    vals = struct.unpack(f'>{num_points * 3}f', points_data)
    positions = [(vals[i * 3], vals[i * 3 + 1]) for i in range(num_points)]
    return positions, rest_bytes


def _read_velocities(rest_bytes, num_points):
    """FIELD 섹션에서 velocity 배열을 읽는다. 없으면 0 벡터"""
    velocities = [(0.0, 0.0)] * num_points
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
                vel_vals = struct.unpack(f'>{ncomp * ntuples}f', vel_bytes)
                velocities = [(vel_vals[i * ncomp], vel_vals[i * ncomp + 1])
                              for i in range(ntuples)]

            cursor += data_size
            while cursor < len(header_text) and header_text[cursor] == '\n':
                cursor += 1
    except Exception:
        pass
    return velocities


def _compute_densities(positions):
    """spatial hash로 반경 내 이웃 수 계산 → (valid, densities, max_density)"""
    num_points = len(positions)
    cell_size = DENSITY_RADIUS
    grid_map = {}
    valid = [False] * num_points
    for i in range(num_points):
        px, py = positions[i]
        if not (math.isfinite(px) and math.isfinite(py)):
            continue
        valid[i] = True
        cx = int(math.floor(px / cell_size))
        cy = int(math.floor(py / cell_size))
        grid_map.setdefault((cx, cy), []).append(i)

    densities = [0.0] * num_points
    r_sq = DENSITY_RADIUS * DENSITY_RADIUS
    for i in range(num_points):
        if not valid[i]:
            continue
        px_i, py_i = positions[i]
        cx = int(math.floor(px_i / cell_size))
        cy = int(math.floor(py_i / cell_size))
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for j in grid_map.get((cx + dx, cy + dy), []):
                    if j == i:
                        continue
                    ddx = positions[j][0] - px_i
                    ddy = positions[j][1] - py_i
                    if ddx * ddx + ddy * ddy <= r_sq:
                        count += 1
        densities[i] = float(count)

    max_density = max(densities) if densities else 1.0
    if max_density < 1.0:
        max_density = 1.0
    return valid, densities, max_density


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


def load_stick_figure(filepath):
    """VTK 파일 로드 → 3D 스틱피겨 vtkAssembly (실패/입자 없음 시 None)"""
    if not Path(filepath).exists():
        return None

    step_match = re.search(r'_(\d+)\.vtk$', str(filepath))
    step_num = int(step_match.group(1)) if step_match else 0

    positions, rest_bytes = _read_points(filepath)
    if positions is None:
        return None
    num_points = len(positions)

    valid, densities, max_density = _compute_densities(positions)
    velocities = _read_velocities(rest_bytes, num_points)

    line_points = vtk.vtkPoints()
    line_cells = vtk.vtkCellArray()
    line_scalars = vtk.vtkFloatArray()
    line_scalars.SetName('density')

    head_points = vtk.vtkPoints()
    head_scalars = vtk.vtkFloatArray()
    head_scalars.SetName('density')

    shadow_points = vtk.vtkPoints()
    shadow_cells = vtk.vtkCellArray()

    for i in range(num_points):
        px, py = positions[i]
        if not valid[i]:
            continue
        vx, vy = velocities[i]
        speed = math.sqrt(vx * vx + vy * vy)

        if speed > 0.01:
            angle = math.atan2(vy, vx) - math.pi / 2
        else:
            angle = 0.0

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        def w(lx, ly, lz):
            """로컬→월드: XY를 angle만큼 회전, Z는 높이"""
            wx = lx * cos_a - ly * sin_a + px
            wy = lx * sin_a + ly * cos_a + py
            return (wx, wy, lz)

        phase = step_num * 0.5 + i * 1.7
        swing = math.sin(phase) * 0.35
        arm_swing = -swing

        feet_z = 0.0
        hip_z = H * 0.45
        neck_z = H * 0.78
        head_z = H * 0.90

        hip = w(0, 0, hip_z)
        neck = w(0, 0, neck_z)

        l_foot = w(-H * 0.1, swing * H * 0.25, feet_z)
        r_foot = w(H * 0.1, -swing * H * 0.25, feet_z)
        l_knee = w(-H * 0.08, swing * H * 0.1, hip_z * 0.5)
        r_knee = w(H * 0.08, -swing * H * 0.1, hip_z * 0.5)

        l_shoulder = w(-H * 0.15, 0, neck_z)
        r_shoulder = w(H * 0.15, 0, neck_z)
        l_hand = w(-H * 0.18, arm_swing * H * 0.25, H * 0.50)
        r_hand = w(H * 0.18, -arm_swing * H * 0.25, H * 0.50)

        head_center = w(0, 0, head_z)

        density_val = densities[i]

        def add_seg(p1, p2):
            id1 = line_points.InsertNextPoint(*p1)
            id2 = line_points.InsertNextPoint(*p2)
            seg = vtk.vtkLine()
            seg.GetPointIds().SetId(0, id1)
            seg.GetPointIds().SetId(1, id2)
            line_cells.InsertNextCell(seg)
            line_scalars.InsertNextValue(density_val)
            line_scalars.InsertNextValue(density_val)

        add_seg(hip, neck)
        add_seg(l_shoulder, r_shoulder)
        add_seg(hip, l_knee)
        add_seg(l_knee, l_foot)
        add_seg(hip, r_knee)
        add_seg(r_knee, r_foot)
        add_seg(l_shoulder, l_hand)
        add_seg(r_shoulder, r_hand)

        head_points.InsertNextPoint(*head_center)
        head_scalars.InsertNextValue(density_val)

        shadow_pts = [hip, neck, l_shoulder, r_shoulder,
                      l_knee, r_knee, l_foot, r_foot, l_hand, r_hand]
        shadow_flat = [(p[0], p[1], 0.001) for p in shadow_pts]
        shadow_segs = [(0, 1), (2, 3), (0, 4), (4, 6), (0, 5), (5, 7), (2, 8), (3, 9)]
        for s1, s2 in shadow_segs:
            id1 = shadow_points.InsertNextPoint(*shadow_flat[s1])
            id2 = shadow_points.InsertNextPoint(*shadow_flat[s2])
            seg = vtk.vtkLine()
            seg.GetPointIds().SetId(0, id1)
            seg.GetPointIds().SetId(1, id2)
            shadow_cells.InsertNextCell(seg)

    lut = _build_lut(max_density)

    line_poly = vtk.vtkPolyData()
    line_poly.SetPoints(line_points)
    line_poly.SetLines(line_cells)
    line_poly.GetPointData().SetScalars(line_scalars)

    tube = vtk.vtkTubeFilter()
    tube.SetInputData(line_poly)
    tube.SetRadius(TUBE_R)
    tube.SetNumberOfSides(6)
    tube.CappingOn()
    tube.Update()

    body_mapper = vtk.vtkPolyDataMapper()
    body_mapper.SetInputConnection(tube.GetOutputPort())
    body_mapper.SetScalarModeToUsePointData()
    body_mapper.SetLookupTable(lut)
    body_mapper.SetScalarRange(0.0, max_density)

    body_actor = vtk.vtkActor()
    body_actor.SetMapper(body_mapper)

    head_poly = vtk.vtkPolyData()
    head_poly.SetPoints(head_points)
    head_poly.GetPointData().SetScalars(head_scalars)

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

    shadow_poly = vtk.vtkPolyData()
    shadow_poly.SetPoints(shadow_points)
    shadow_poly.SetLines(shadow_cells)

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
