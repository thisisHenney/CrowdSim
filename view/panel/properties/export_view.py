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
        # .ui 생성 코드가 radioButton_5/6을 둘 다 setChecked(True)로 만드는데,
        # 같은 부모 밑이라 Qt가 자동 상호배타 그룹을 만들어 마지막에 설정된
        # radioButton_6("구간 설정")가 기본 선택으로 남는다. "전체"를 기본으로 강제한다.
        ui.radioButton_5.setChecked(True)

        ui.pushButton.clicked.connect(self._clicked_export_result_data)
        ui.pushButton_3.clicked.connect(self._clicked_export_video)
        ui.pushButton_2.clicked.connect(self._clicked_export_image_sequence)

    def _clicked_export_result_data(self):
        """결과 폴더의 원본 VTK 파일을 프레임 범위만큼 다른 폴더로 복사"""
        parent = self._parent
        ui = self.ui
        anim_steps = getattr(parent, '_anim_steps', None)
        anim_files = getattr(parent, '_anim_files', None)
        if not anim_steps or not anim_files:
            from nextlib.widgets.messagebox import messagebox_warning
            messagebox_warning(parent,
                               '내보낼 결과 파일이 없습니다.\n케이스를 열거나 해석을 실행한 뒤 다시 시도해주세요.')
            return

        total = len(anim_steps)
        if ui.radioButton_6.isChecked():
            try:
                start = int(ui.lineEdit_5.text())
                end = int(ui.lineEdit_12.text())
            except ValueError:
                from nextlib.widgets.messagebox import messagebox_warning
                messagebox_warning(parent, '시작/종료 프레임은 숫자로 입력해주세요.')
                return
            start = max(1, min(start, total))
            end = max(start, min(end, total))
        else:
            start, end = 1, total

        from PySide6.QtWidgets import QFileDialog, QProgressDialog, QApplication

        dest_dir = QFileDialog.getExistingDirectory(parent, '해석 결과 저장 폴더 선택')
        if not dest_dir:
            return

        import shutil

        # 선택된 프레임 범위(1-based, 양끝 포함)에 해당하는 원본 VTK 경로 전부 수집 (전체 grid 포함)
        src_files = []
        for step in anim_steps[start - 1:end]:
            for filepath in anim_files.get(step, {}).values():
                src_files.append(filepath)

        progress = QProgressDialog(
            f'해석 결과 복사 중... (프레임 {start}~{end})', '취소', 0, len(src_files), parent)
        progress.setWindowTitle('해석 결과 내보내기')
        progress.setMinimumDuration(0)
        progress.setValue(0)

        copied = 0
        try:
            for i, filepath in enumerate(src_files):
                if progress.wasCanceled():
                    break
                src = Path(filepath)
                if src.is_file():
                    shutil.copy2(src, Path(dest_dir) / src.name)
                    copied += 1
                progress.setValue(i + 1)
                QApplication.processEvents()
        finally:
            progress.close()
            parent._ui.statusbar.showMessage(
                f'해석 결과 내보내기 완료: {copied}개 파일 -> {dest_dir}')

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
