"""결과 애니메이션 재생 바 (UI 구성 + 재생/프리로드/스캔 로직)

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.vtk, self.prj, self._ui (statusbar)
"""
import re
from pathlib import Path

from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QSlider, QToolButton,
                               QStyleOptionSlider, QStyle, QSpinBox, QComboBox)
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QPen, QPolygonF

from view.main.stick_figure import load_stick_figure


class _ClickSlider(QSlider):
    """클릭한 위치로 바로 이동 + 드래그 가능한 슬라이더"""
    def _pos_to_value(self, pos_x):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        groove = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt,
                                             QStyle.SubControl.SC_SliderGroove, self)
        handle = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, opt,
                                             QStyle.SubControl.SC_SliderHandle, self)
        slider_len = groove.width() - handle.width()
        offset = groove.x() + handle.width() // 2
        val = self.minimum() + (self.maximum() - self.minimum()) * (pos_x - offset) / max(slider_len, 1)
        return max(self.minimum(), min(self.maximum(), round(val)))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setValue(self._pos_to_value(event.position().x()))
            self._dragging = True
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if getattr(self, '_dragging', False):
            self.setValue(self._pos_to_value(event.position().x()))
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)


def _make_anim_icon(draw_func, size=16):
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(50, 50, 50))
    draw_func(p, size)
    p.end()
    return QIcon(pix)


def _draw_first(p, s):
    # ◀◀
    tri1 = QPolygonF([QPointF(s - 1, 2), QPointF(s - 1, s - 2), QPointF(s / 2, s / 2)])
    p.drawPolygon(tri1)
    tri2 = QPolygonF([QPointF(s / 2, 2), QPointF(s / 2, s - 2), QPointF(1, s / 2)])
    p.drawPolygon(tri2)


def _draw_prev(p, s):
    # |◀
    p.drawRect(1, 2, 2, s - 4)
    tri = QPolygonF([QPointF(s - 2, 2), QPointF(s - 2, s - 2), QPointF(4, s / 2)])
    p.drawPolygon(tri)


def _draw_play(p, s):
    # ▶
    tri = QPolygonF([QPointF(3, 2), QPointF(3, s - 2), QPointF(s - 3, s / 2)])
    p.drawPolygon(tri)


def _draw_stop(p, s):
    # ■
    p.drawRect(3, 3, s - 6, s - 6)


def _draw_next(p, s):
    # ▶|
    tri = QPolygonF([QPointF(2, 2), QPointF(2, s - 2), QPointF(s - 4, s / 2)])
    p.drawPolygon(tri)
    p.drawRect(s - 3, 2, 2, s - 4)


def _draw_last(p, s):
    # ▶▶
    tri1 = QPolygonF([QPointF(1, 2), QPointF(1, s - 2), QPointF(s / 2, s / 2)])
    p.drawPolygon(tri1)
    tri2 = QPolygonF([QPointF(s / 2, 2), QPointF(s / 2, s - 2), QPointF(s - 1, s / 2)])
    p.drawPolygon(tri2)


def _draw_reload(p, s):
    # 원형 화살표 (리로드)
    pen = QPen(QColor(50, 50, 50), 2.0)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawArc(QRectF(2, 2, s - 4, s - 4), 60 * 16, 270 * 16)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(50, 50, 50))
    arrow = QPolygonF([QPointF(s / 2 + 1, 1), QPointF(s / 2 + 1, 6), QPointF(s / 2 + 5, 3.5)])
    p.drawPolygon(arrow)


def _draw_record(pix_size=16):
    pix = QPixmap(pix_size, pix_size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(240, 150, 30))
    p.drawEllipse(1, 1, 14, 14)
    p.end()
    return QIcon(pix)


_BTN_STYLE = ('QToolButton { border: 1px solid #ccc; border-radius: 3px; background: white; }'
              ' QToolButton:hover { background: #e8e8e8; }')

_SLIDER_STYLE = (
    'QSlider::groove:horizontal {'
    '  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,'
    '    stop:0 #b0c4de, stop:1 #dce6f0);'
    '  height: 6px;'
    '  border-radius: 3px;'
    '}'
    'QSlider::sub-page:horizontal {'
    '  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,'
    '    stop:0 #4a90d9, stop:1 #6aace0);'
    '  height: 6px;'
    '  border-radius: 3px;'
    '}'
    'QSlider::handle:horizontal {'
    '  background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,'
    '    fx:0.4, fy:0.4, stop:0 #ffffff, stop:1 #4a90d9);'
    '  width: 14px;'
    '  height: 14px;'
    '  margin: -5px 0;'
    '  border-radius: 7px;'
    '  border: 1px solid #3a7abd;'
    '}'
    'QSlider::handle:horizontal:hover {'
    '  background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,'
    '    fx:0.4, fy:0.4, stop:0 #ffffff, stop:1 #3a7abd);'
    '  border: 1px solid #2a5a9d;'
    '}'
    'QSlider::tick-mark:horizontal {'
    '  background: #888;'
    '  width: 1px;'
    '  height: 6px;'
    '}')


class AnimationMixin:
    """애니메이션 재생 바 + 결과 스캔/프리로드/재생 로직"""

    def _create_anim_bar(self):
        """재생 바 QFrame을 생성해 반환하고 관련 상태를 초기화"""
        self._anim_bar = QFrame()
        self._anim_bar.setFixedHeight(32)
        self._anim_bar.setStyleSheet(
            "QFrame { background: transparent; border: none; border-top: 1px solid #d0d7de; }")
        anim_layout = QHBoxLayout(self._anim_bar)
        anim_layout.setContentsMargins(6, 2, 6, 2)
        anim_layout.setSpacing(4)

        self._icon_play = _make_anim_icon(_draw_play)
        self._icon_stop = _make_anim_icon(_draw_stop)

        def _tool_button(icon, tooltip, handler):
            btn = QToolButton()
            btn.setIcon(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(28, 24)
            btn.setStyleSheet(_BTN_STYLE)
            btn.clicked.connect(handler)
            return btn

        self._btn_anim_reload = _tool_button(_make_anim_icon(_draw_reload), '결과 다시 읽기', self._anim_reload)
        self._btn_anim_first = _tool_button(_make_anim_icon(_draw_first), '처음으로', self._anim_first)
        self._btn_anim_prev = _tool_button(_make_anim_icon(_draw_prev), '이전 프레임', self._anim_prev)
        self._btn_anim_play = _tool_button(self._icon_play, '재생 / 정지', self._anim_play_pause)
        self._btn_anim_next = _tool_button(_make_anim_icon(_draw_next), '다음 프레임', self._anim_next)
        self._btn_anim_last = _tool_button(_make_anim_icon(_draw_last), '끝으로', self._anim_last)
        self._btn_anim_record = _tool_button(_draw_record(), '동영상 저장', self._anim_export_video)

        self._anim_slider = _ClickSlider(Qt.Orientation.Horizontal)
        self._anim_slider.setMinimum(0)
        self._anim_slider.setMaximum(0)
        self._anim_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._anim_slider.setTickInterval(1)  # _scan_vtk_results에서 재설정
        self._anim_slider.setStyleSheet(_SLIDER_STYLE)
        self._anim_slider.valueChanged.connect(self._anim_slider_changed)

        self._anim_spin = QSpinBox()
        self._anim_spin.setMinimum(0)
        self._anim_spin.setMaximum(0)
        self._anim_spin.setFixedWidth(60)
        self._anim_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._anim_spin.setStyleSheet('font-size: 11px;')
        self._anim_spin.valueChanged.connect(self._anim_spin_changed)

        self._anim_total_label = QLabel('/ 0')
        self._anim_total_label.setFixedWidth(45)
        self._anim_total_label.setStyleSheet('font-size: 11px;')

        self._anim_speed_combo = QComboBox()
        self._anim_speed_combo.addItems(['x1', 'x1.5', 'x2', 'x4', 'x8', 'x16', 'x32', 'x64'])
        self._anim_speed_combo.setFixedWidth(55)
        self._anim_speed_combo.setToolTip('재생 속도')
        self._anim_speed_combo.setStyleSheet('font-size: 11px;')
        self._anim_speed_combo.currentIndexChanged.connect(self._anim_speed_changed)
        self._anim_speed_ms = 200  # 기본 x1 = 200ms

        anim_layout.addWidget(self._btn_anim_reload)
        anim_layout.addWidget(self._btn_anim_first)
        anim_layout.addWidget(self._btn_anim_prev)
        anim_layout.addWidget(self._btn_anim_play)
        anim_layout.addWidget(self._btn_anim_next)
        anim_layout.addWidget(self._btn_anim_last)
        anim_layout.addWidget(self._anim_slider, 1)
        anim_layout.addWidget(self._anim_spin)
        anim_layout.addWidget(self._anim_total_label)
        anim_layout.addWidget(self._anim_speed_combo)
        anim_layout.addWidget(self._btn_anim_record)

        self._anim_bar.setVisible(False)

        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_timer = QTimer()
        self._anim_timer.timeout.connect(self._anim_tick)
        self._anim_playing = False
        self._preload_timer = None

        return self._anim_bar

    def _anim_reset(self):
        """애니메이션 상태와 컨트롤을 초기 상태로 되돌림"""
        self._anim_stop_play()
        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}
        self._anim_slider.setValue(0)
        self._anim_slider.setMaximum(0)
        self._anim_spin.blockSignals(True)
        self._anim_spin.setMaximum(0)
        self._anim_spin.setValue(0)
        self._anim_spin.blockSignals(False)
        self._anim_total_label.setText('/ 0')
        self._anim_bar.setVisible(False)

    def _scan_vtk_results(self):
        """케이스 열 때 기존 VTK 결과 파일 스캔"""
        self._anim_stop_play()
        self._anim_steps = []
        self._anim_files = {}
        self._anim_cache = {}

        result_dir = Path(self.prj.path) / self.prj.name
        if not result_dir.is_dir():
            self._anim_bar.setVisible(False)
            return

        for vtk_file in result_dir.glob('*.vtk'):
            match = re.search(r'_grid(\d+)_(\d+)\.vtk$', vtk_file.name)
            if not match:
                continue
            grid_num = int(match.group(1))
            step = int(match.group(2))

            if step not in self._anim_files:
                self._anim_files[step] = {}
            self._anim_files[step][grid_num] = str(vtk_file)

        if self._anim_files:
            self._anim_steps = sorted(self._anim_files.keys())
            total = len(self._anim_steps)
            self._anim_slider.setMaximum(total - 1)
            self._anim_slider.setTickInterval(max(1, total // 2))
            self._anim_spin.setMinimum(1)
            self._anim_spin.setMaximum(total)
            self._anim_total_label.setText(f'/ {total}')
            self._anim_slider.setValue(0)
            self._anim_bar.setVisible(True)
            self._anim_show_step(0)
            self._set_2d_view()
            self._anim_preload()
        else:
            self._anim_bar.setVisible(False)

    def _set_2d_view(self):
        """카메라를 기본 뷰로 설정 (X 오른쪽, Y 위쪽, Z 앞쪽)"""
        cam = self.vtk.renderer.GetActiveCamera()
        cam.ParallelProjectionOff()
        cam.SetPosition(0, 0, 1)
        cam.SetFocalPoint(0, 0, 0)
        cam.SetViewUp(0, 1, 0)
        self.vtk.renderer.ResetCamera()
        self.vtk.vtk_widget.GetRenderWindow().Render()

    def update_solver_file(self, file_name, added_files, removed_files):
        """DirectoryWatcher 콜백: 솔버가 만든 새 결과 파일을 재생 바에 반영"""
        if not added_files:
            return

        for recent_file in added_files:
            if not recent_file.endswith('.vtk'):
                continue

            match = re.search(r'_grid(\d+)_(\d+)\.vtk$', recent_file)
            if not match:
                continue

            grid_num = int(match.group(1))
            step = int(match.group(2))

            if step not in self._anim_files:
                self._anim_files[step] = {}
            self._anim_files[step][grid_num] = recent_file

            if step not in self._anim_steps:
                self._anim_steps.append(step)
                self._anim_steps.sort()
                total = len(self._anim_steps)
                self._anim_slider.setMaximum(total - 1)
                self._anim_slider.setTickInterval(max(1, total // 2))
                self._anim_spin.setMaximum(total)
                self._anim_total_label.setText(f'/ {total}')
                self._anim_bar.setVisible(True)

        if self._anim_steps:
            last_idx = len(self._anim_steps) - 1
            if self._anim_slider.value() == last_idx:
                # 같은 값이면 시그널 안 나오므로 직접 호출
                self._anim_show_step(last_idx)
            else:
                self._anim_slider.setValue(last_idx)

    def _anim_reload(self):
        """결과 파일 다시 스캔"""
        self._anim_stop_play()
        self._scan_vtk_results()
        self._ui.statusbar.showMessage('결과 파일을 다시 읽었습니다.')
        self._anim_preload()

    def _anim_preload(self):
        """백그라운드에서 전체 프레임 캐시에 프리로드"""
        if not self._anim_steps:
            return
        # 이미 프리로드 중이면 중단
        if self._preload_timer is not None:
            self._preload_timer.stop()

        self._preload_total = len(self._anim_steps)
        # 이미 캐시된 프레임 건너뛰기
        self._preload_queue = [i for i, s in enumerate(self._anim_steps) if s not in self._anim_cache]
        if not self._preload_queue:
            self._ui.statusbar.showMessage(f'전체 {self._preload_total} 프레임 캐시 완료')
            return

        self._ui.statusbar.showMessage(f'프레임 프리로드 중... 0 / {len(self._preload_queue)}')
        self._preload_timer = QTimer()
        self._preload_timer.timeout.connect(self._preload_tick)
        self._preload_timer.start(0)  # 가능한 빠르게, 하지만 UI 블로킹 없이

    def _stop_preload(self):
        if self._preload_timer is not None:
            self._preload_timer.stop()
            self._preload_timer = None

    def _preload_tick(self):
        """한 프레임씩 캐시에 로드"""
        if not self._preload_queue:
            self._preload_timer.stop()
            self._preload_timer = None
            self._ui.statusbar.showMessage(f'전체 {self._preload_total} 프레임 프리로드 완료')
            return

        idx = self._preload_queue.pop(0)
        step = self._anim_steps[idx]
        if step not in self._anim_cache:
            files = self._anim_files.get(step, {})
            actors = {}
            for grid_num, filepath in files.items():
                actor = load_stick_figure(filepath)
                if actor:
                    actors[grid_num] = actor
            self._anim_cache[step] = actors

        loaded = self._preload_total - len(self._preload_queue)
        self._ui.statusbar.showMessage(f'프레임 프리로드 중... {loaded} / {self._preload_total}')

    def _anim_show_step(self, slider_index):
        """주어진 슬라이더 인덱스의 step을 VTK에 표시"""
        if not self._anim_steps or slider_index < 0 or slider_index >= len(self._anim_steps):
            return

        step = self._anim_steps[slider_index]
        files = self._anim_files.get(step, {})

        # 캐시에서 actor 가져오거나 새로 로드
        if step in self._anim_cache:
            new_actors = self._anim_cache[step]
        else:
            new_actors = {}
            for grid_num, filepath in files.items():
                actor = load_stick_figure(filepath)
                if actor:
                    new_actors[grid_num] = actor

            # 파일을 하나도 로드하지 못한 경우 재생 중지
            if files and not new_actors:
                self._anim_stop_play()
                self._ui.statusbar.showMessage('결과 파일을 찾을 수 없습니다. 경로를 확인해주세요.')
                return

            self._anim_cache[step] = new_actors

        cam = self.vtk.renderer.GetActiveCamera()
        cam_pos = cam.GetPosition()
        cam_focal = cam.GetFocalPoint()
        cam_up = cam.GetViewUp()
        cam_scale = cam.GetParallelScale()

        render_window = self.vtk.vtk_widget.GetRenderWindow()
        render_window.SetSwapBuffers(False)

        all_grids = set()
        for s in self._anim_files.values():
            all_grids.update(s.keys())
        for grid_num in all_grids:
            self.vtk.obj_manager.group(f'grid{grid_num}').remove()

        for grid_num, actor in new_actors.items():
            self.vtk.obj_manager.add_plain(
                actor, name=f'grid{grid_num}_{step}', group=f'grid{grid_num}')

        cam.SetPosition(cam_pos)
        cam.SetFocalPoint(cam_focal)
        cam.SetViewUp(cam_up)
        cam.SetParallelScale(cam_scale)
        self.vtk.renderer.ResetCameraClippingRange()

        render_window.SetSwapBuffers(True)
        render_window.Render()

        self._anim_spin.blockSignals(True)
        self._anim_spin.setMaximum(len(self._anim_steps))
        self._anim_spin.setValue(slider_index + 1)
        self._anim_spin.blockSignals(False)
        self._anim_total_label.setText(f'/ {len(self._anim_steps)}')

    def _anim_slider_changed(self, value):
        self._anim_show_step(value)

    def _anim_spin_changed(self, value):
        """스핀박스에서 프레임 번호 직접 입력 시"""
        self._anim_slider.setValue(value - 1)

    def _anim_first(self):
        self._anim_stop_play()
        self._anim_slider.setValue(0)

    def _anim_prev(self):
        self._anim_stop_play()
        v = self._anim_slider.value()
        if v > 0:
            self._anim_slider.setValue(v - 1)

    def _anim_next(self):
        self._anim_stop_play()
        v = self._anim_slider.value()
        if v < self._anim_slider.maximum():
            self._anim_slider.setValue(v + 1)

    def _anim_last(self):
        self._anim_stop_play()
        self._anim_slider.setValue(self._anim_slider.maximum())

    def _anim_play_pause(self):
        if self._anim_playing:
            self._anim_stop_play()
        else:
            self._anim_playing = True
            self._btn_anim_play.setIcon(self._icon_stop)
            self._anim_timer.start(self._anim_speed_ms)

    def _anim_speed_changed(self, index):
        speeds = {0: 200, 1: 133, 2: 100, 3: 50, 4: 25, 5: 12, 6: 6, 7: 3}  # x1~x64
        self._anim_speed_ms = speeds.get(index, 200)
        if self._anim_playing:
            self._anim_timer.start(self._anim_speed_ms)

    def _anim_stop_play(self):
        self._anim_playing = False
        self._anim_timer.stop()
        self._btn_anim_play.setIcon(self._icon_play)

    def _anim_tick(self):
        v = self._anim_slider.value()
        if v < self._anim_slider.maximum():
            self._anim_slider.setValue(v + 1)
        else:
            self._anim_slider.setValue(0)
