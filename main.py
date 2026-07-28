import os
os.environ["QT_LOGGING_RULES"] = "qt.gui.imageio=false"
import signal
import sys
from pathlib import Path
from dataclasses import dataclass

# 프로젝트 동봉 lib/(nextlib 등)을 최우선으로 사용 - 외부 경로/PYTHONPATH에 의존하지 않음
sys.path.insert(0, str(Path(__file__).resolve().parent / 'lib'))

from PySide6.QtCore import QTimer
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

    # 터미널에서 Ctrl+C(SIGINT)를 누르면 Qt 이벤트 루프 도중 아무 콜백에나
    # KeyboardInterrupt가 발생해 지저분한 트레이스백이 찍히고 앱이 비정상 종료된다.
    # 대신 조용히 안내 메시지를 찍고 정상적으로 앱을 닫는다.
    def _handle_sigint(signum, frame):
        print('\n[CrowdSim] 종료 요청(Ctrl+C)을 받아 프로그램을 닫습니다...')
        app.quit()

    signal.signal(signal.SIGINT, _handle_sigint)

    # Qt의 C++ 이벤트 루프는 Python 시그널 처리를 위해 주기적으로 인터프리터에
    # 제어를 돌려줘야 하는데, 아무 QTimer도 안 돌고 있으면 그 기회가 안 생겨서
    # Ctrl+C가 한참 뒤에야(다음 GUI 상호작용 시점에) 반영된다. 항상 도는 빈 타이머로
    # 그 기회를 주기적으로 만들어준다.
    _sigint_pump = QTimer()
    _sigint_pump.timeout.connect(lambda: None)
    _sigint_pump.start(200)

    start_path = ''
    # start_path = r'%UserProfile%\Desktop\TestCase\111'    # for Windows

    if len(sys.argv) == 2:
        start_path = sys.argv[1]

    crowd = Crowd()
    crowd.start(start_path)
    app.exec()



