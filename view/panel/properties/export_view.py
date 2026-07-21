from pathlib import Path

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
        ui.pushButton_3.clicked.connect(self._clicked_export_video)
        ui.pushButton_2.clicked.connect(self._clicked_export_image_sequence)

    def _clicked_export_video(self):
        """기존 애니메이션 바의 동영상 내보내기 기능을 그대로 호출"""
        if hasattr(self._parent, '_anim_export_video'):
            self._parent._anim_export_video()

    def _clicked_export_image_sequence(self):
        """현재 뷰포트를 프레임 범위만큼 PNG 이미지 시퀀스로 저장"""
        parent = self._parent
        anim_steps = getattr(parent, '_anim_steps', None)
        if not anim_steps:
            return

        from PySide6.QtWidgets import QFileDialog, QInputDialog, QProgressDialog, QApplication

        total = len(anim_steps)
        start, ok = QInputDialog.getInt(
            parent, '이미지 시퀀스 내보내기', f'시작 프레임 (1~{total}):', 1, 1, total)
        if not ok:
            return
        end, ok = QInputDialog.getInt(
            parent, '이미지 시퀀스 내보내기', f'끝 프레임 ({start}~{total}):', total, start, total)
        if not ok:
            return

        dest_dir = QFileDialog.getExistingDirectory(parent, '이미지 저장 폴더 선택')
        if not dest_dir:
            return

        parent._anim_stop_play()

        import vtk

        render_window = parent.vtk.vtk_widget.GetRenderWindow()
        interactor = render_window.GetInteractor()
        interactor.Disable()
        parent.vtk.vtk_widget.setEnabled(False)

        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(render_window)
        w2i.SetInputBufferTypeToRGB()
        w2i.ReadFrontBufferOff()

        writer = vtk.vtkPNGWriter()
        writer.SetInputConnection(w2i.GetOutputPort())

        progress = QProgressDialog(
            f'이미지 저장 중... (프레임 {start}~{end})', '취소', 0, end - start, parent)
        progress.setWindowTitle('이미지 내보내기')
        progress.setMinimumDuration(0)
        progress.setValue(0)

        name = parent.prj.name
        try:
            for i, frame in enumerate(range(start - 1, end)):
                if progress.wasCanceled():
                    break

                parent._anim_show_step(frame)
                render_window.Render()
                w2i.Modified()
                w2i.Update()

                filepath = str(Path(dest_dir) / f'{name}_{frame + 1:04d}.png')
                writer.SetFileName(filepath)
                writer.Write()

                progress.setValue(i + 1)
                QApplication.processEvents()
        finally:
            progress.close()
            interactor.Enable()
            parent.vtk.vtk_widget.setEnabled(True)
            parent._ui.statusbar.showMessage(f'이미지 시퀀스 저장 완료: {dest_dir}')

    def get_widget(self):
        return self.ui.widget

    def save_input_file(self, solver):
        return solver

    def load_input_file(self, solver):
        pass
