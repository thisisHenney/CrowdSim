"""애니메이션을 동영상(MP4/AVI)으로 내보내기

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.vtk, self.prj, self._ui (statusbar), self._anim_bar, self._anim_slider,
self._anim_steps, self._anim_stop_play(), self._anim_show_step()
"""
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QRadioButton,
                               QGroupBox, QLabel, QSpinBox, QPushButton,
                               QFileDialog, QProgressDialog, QApplication, QMessageBox)


class VideoExportMixin:
    """프레임 범위/화질 선택 후 오프스크린 렌더링으로 동영상 저장"""

    def _anim_export_video(self):
        """동영상 내보내기 설정 다이얼로그 표시"""
        if not self._anim_steps:
            return

        self._anim_stop_play()

        # 이미 열려있으면 포커스만
        if getattr(self, '_export_dlg', None) is not None:
            self._export_dlg.raise_()
            self._export_dlg.activateWindow()
            return

        total = len(self._anim_steps)

        dlg = QDialog(self)
        dlg.setWindowTitle('동영상 내보내기')
        dlg.setFixedWidth(350)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        layout = QVBoxLayout(dlg)

        # 프레임 범위 선택
        range_box = QGroupBox(f'프레임 범위 (전체: 1 ~ {total})')
        range_grid = QVBoxLayout(range_box)

        start_row = QHBoxLayout()
        start_row.addWidget(QLabel('시작:'))
        spin_start = QSpinBox()
        spin_start.setMinimum(1)
        spin_start.setMaximum(total)
        spin_start.setValue(1)
        spin_start.setFixedWidth(70)
        start_row.addWidget(spin_start)
        btn_set_start = QPushButton('현재 프레임')
        btn_set_start.setFixedWidth(100)
        btn_set_start.clicked.connect(lambda: spin_start.setValue(self._anim_slider.value() + 1))
        start_row.addWidget(btn_set_start)
        range_grid.addLayout(start_row)

        end_row = QHBoxLayout()
        end_row.addWidget(QLabel('끝:    '))
        spin_end = QSpinBox()
        spin_end.setMinimum(1)
        spin_end.setMaximum(total)
        spin_end.setValue(total)
        spin_end.setFixedWidth(70)
        end_row.addWidget(spin_end)
        btn_set_end = QPushButton('현재 프레임')
        btn_set_end.setFixedWidth(100)
        btn_set_end.clicked.connect(lambda: spin_end.setValue(self._anim_slider.value() + 1))
        end_row.addWidget(btn_set_end)
        range_grid.addLayout(end_row)

        layout.addWidget(range_box)

        # 시작 > 끝 방지
        spin_start.valueChanged.connect(lambda v: spin_end.setValue(max(v, spin_end.value())))
        spin_end.valueChanged.connect(lambda v: spin_start.setValue(min(v, spin_start.value())))

        # 화질 선택
        group_box = QGroupBox('화질 선택')
        group_layout = QVBoxLayout(group_box)
        btn_mid = QRadioButton('중간 품질 (1x)')
        btn_good = QRadioButton('높은 품질 (1.5x)')
        btn_high = QRadioButton('원본급 (2x)')
        btn_good.setChecked(True)
        group_layout.addWidget(btn_mid)
        group_layout.addWidget(btn_good)
        group_layout.addWidget(btn_high)
        layout.addWidget(group_box)

        # 버튼
        btn_row = QHBoxLayout()
        btn_export = QPushButton('내보내기')
        btn_export.setDefault(True)
        btn_cancel = QPushButton('취소')
        btn_row.addStretch()
        btn_row.addWidget(btn_export)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        btn_cancel.clicked.connect(dlg.close)

        def do_export():
            frame_start = spin_start.value() - 1
            frame_end = spin_end.value()
            if btn_high.isChecked():
                scale_factor = 2
            elif btn_good.isChecked():
                scale_factor = 1.5
            else:
                scale_factor = 1
            dlg.close()
            self._do_anim_export(frame_start, frame_end, scale_factor)

        btn_export.clicked.connect(do_export)

        self._export_dlg = dlg
        dlg.destroyed.connect(lambda: setattr(self, '_export_dlg', None))
        dlg.show()

    def _do_anim_export(self, frame_start, frame_end, scale_factor):
        """실제 동영상 내보내기 실행"""
        default_path = str(Path(self.prj.path) / f'{self.prj.name}_animation.mp4')
        filepath, _ = QFileDialog.getSaveFileName(
            self, '동영상 저장', default_path,
            'MP4 Video (*.mp4);;AVI Video (*.avi)')
        if not filepath:
            return

        import vtk

        render_window = self.vtk.vtk_widget.GetRenderWindow()
        orig_size = render_window.GetSize()

        interactor = render_window.GetInteractor()
        interactor.Disable()
        self.vtk.vtk_widget.setEnabled(False)
        self._anim_bar.setEnabled(False)

        # 카메라 상태를 리사이즈 전에 저장
        cam = self.vtk.renderer.GetActiveCamera()
        cam_pos = cam.GetPosition()
        cam_focal = cam.GetFocalPoint()
        cam_up = cam.GetViewUp()
        cam_scale = cam.GetParallelScale()

        # 오프스크린으로 전환하여 화면 깜빡임 방지
        render_window.SetOffScreenRendering(True)

        if scale_factor > 1:
            render_window.SetSize(int(orig_size[0] * scale_factor), int(orig_size[1] * scale_factor))

        def _restore_cam():
            cam.SetPosition(cam_pos)
            cam.SetFocalPoint(cam_focal)
            cam.SetViewUp(cam_up)
            cam.SetParallelScale(cam_scale)
            self.vtk.renderer.ResetCameraClippingRange()

        def _restore_window():
            render_window.SetOffScreenRendering(False)
            if scale_factor > 1:
                render_window.SetSize(orig_size[0], orig_size[1])
            _restore_cam()
            render_window.Render()
            interactor.Enable()
            self.vtk.vtk_widget.setEnabled(True)
            self._anim_bar.setEnabled(True)

        _restore_cam()
        render_window.Render()
        width, height = render_window.GetSize()

        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(render_window)
        w2i.SetInputBufferTypeToRGB()
        w2i.ReadFrontBufferOff()

        export_count = frame_end - frame_start

        progress = QProgressDialog(
            f'동영상 저장 중... (프레임 {frame_start + 1}~{frame_end})', '취소', 0, export_count, self)
        progress.setWindowTitle('동영상 내보내기')
        progress.setMinimumDuration(0)
        progress.setValue(0)

        try:
            import cv2
            import numpy as np
            from vtk.util.numpy_support import vtk_to_numpy

            self._anim_show_step(frame_start)
            _restore_cam()
            render_window.Render()
            w2i.Modified()
            w2i.Update()
            img_data = w2i.GetOutput()
            dims = img_data.GetDimensions()
            width, height = dims[0], dims[1]

            ext = Path(filepath).suffix.lower()
            if ext == '.avi':
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            fps = 5
            writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

            for i in range(frame_start, frame_end):
                if progress.wasCanceled():
                    break

                self._anim_show_step(i)
                _restore_cam()
                render_window.Render()

                w2i.Modified()
                w2i.Update()
                img_data = w2i.GetOutput()

                vtk_array = img_data.GetPointData().GetScalars()
                np_arr = vtk_to_numpy(vtk_array)
                np_arr = np_arr.reshape(height, width, 3)
                np_arr = np.flip(np_arr, axis=0)
                bgr = cv2.cvtColor(np_arr, cv2.COLOR_RGB2BGR)
                writer.write(bgr)

                progress.setValue(i - frame_start + 1)
                QApplication.processEvents()

            writer.release()

        except ImportError:
            # cv2 미설치: VTK 내장 OGV writer로 대체
            progress.close()
            try:
                ogv_writer = vtk.vtkOggTheoraWriter()
                ogv_writer.SetFileName(filepath.replace('.mp4', '.ogv').replace('.avi', '.ogv'))
                ogv_writer.SetInputConnection(w2i.GetOutputPort())
                ogv_writer.SetRate(5)
                ogv_writer.Start()

                for i in range(frame_start, frame_end):
                    self._anim_show_step(i)
                    _restore_cam()
                    render_window.Render()
                    w2i.Modified()
                    w2i.Update()
                    ogv_writer.Write()

                ogv_writer.End()
            except Exception as e:
                QMessageBox.warning(self, '오류',
                                    f'동영상 저장 실패: {e}\ncv2(opencv-python) 설치를 권장합니다.')
                _restore_window()
                return

        _restore_window()
        progress.close()

        quality_labels = {2: '원본급', 1.5: '높은 품질', 1: '중간 품질'}
        quality_label = quality_labels.get(scale_factor, f'{scale_factor}x')
        self._ui.statusbar.showMessage(f'동영상 저장 완료 ({quality_label}, {width}x{height}): {filepath}')
