import os
os.environ["QT_LOGGING_RULES"] = "qt.gui.imageio=false"
import sys
from pathlib import Path
from dataclasses import dataclass

# 프로젝트 동봉 lib/(nextlib 등)을 최우선으로 사용 - 외부 경로/PYTHONPATH에 의존하지 않음
sys.path.insert(0, str(Path(__file__).resolve().parent / 'lib'))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from view.start.start_dialog import StartDialog
from view.theme import build_css


@dataclass
class AppInfor:
    user_path : Path = Path(rf'{Path.home()}\AppData\Local\NEXTfoam')
    path: Path = Path(os.path.dirname(__file__))
    title: str = "Massive Crowd Simulation"
    version: str = "v1.00"


class Crowd:
    def __init__(self):
        self.startDlg = StartDialog(AppInfor)

    def start(self, open_path=''):
        self.startDlg.set_defaults(open_path)
        if not open_path:
            self.startDlg.show()
            self.startDlg.raise_()
            self.startDlg.activateWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(build_css())

    start_path = ''
    # start_path = r'%UserProfile%\Desktop\TestCase\111'    # for Windows

    if len(sys.argv) == 2:
        start_path = sys.argv[1]

    crowd = Crowd()
    crowd.start(start_path)
    app.exec()



