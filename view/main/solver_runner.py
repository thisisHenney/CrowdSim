"""솔버(RuntimeSPH2D) 실행/중단 및 콘솔 출력 수집

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.app_info, self.prj, self.cmd, self.vtk, self.action_run, self.action_stop,
self.solver_watcher, self._anim_reset(), self._load_background_map(),
self.save_input_file(), self.update_solver_file()
"""
import queue
import re
import subprocess
import threading
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor

from nextlib.utils.watcher import DirectoryWatcher

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


class SolverRunMixin:
    """솔버 프로세스 실행/중단과 stdout 실시간 표시"""

    def run_solver(self):
        self.save_input_file()
        self.vtk.obj_manager.all().remove()

        self._anim_reset()
        self._load_background_map()

        solver_exe = str(self.app_info.path / 'solver/e8ight/RuntimeSPH2D/RuntimeSPH2D.exe')
        json_rel = f'.\\{self.prj.name}.json'
        working_path = str(self.prj.path)

        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE: 콘솔 창 숨김

        popen_kwargs = dict(
            cwd=working_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=si,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        self._solver_proc = subprocess.Popen([solver_exe, json_rel], **popen_kwargs)

        self.cmd.add_log_notice(f'Solver started: {self.prj.name}.json')
        self.action_run.setEnabled(False)
        self.action_stop.setEnabled(True)
        self._solver_output_buf = ''

        # 솔버가 자체적으로 %진행률을 안 알려주므로, 실행 중임을 눈에 보이게(계속 움직이는
        # 부정형 진행바) 표시한다. 안 그러면 화면이 멈춘 건지 실행 중인지 구분이 안 된다.
        self._set_solver_progress(running=True)

        combo = self.cmd._ui.comboBox_output_proc_index
        self._console_combo_index = combo.count()
        combo.addItem('Console')
        # 처음 연결된 적 없을 때 무조건 disconnect를 시도하면 최신 PySide6에서
        # RuntimeError 대신 RuntimeWarning만 찍고 넘어가서 try/except로 못 막는다.
        # 실제로 연결한 적 있을 때만 disconnect 하도록 상태를 직접 추적한다.
        if getattr(self, '_output_combo_connected', False):
            combo.currentIndexChanged.disconnect(self._on_output_combo_changed)
        combo.currentIndexChanged.connect(self._on_output_combo_changed)
        self._output_combo_connected = True
        combo.setCurrentIndex(self._console_combo_index)

        # 백그라운드 스레드에서 stdout 읽기
        self._solver_queue = queue.Queue()
        self._solver_reader = threading.Thread(
            target=self._read_solver_stdout, daemon=True)
        self._solver_reader.start()

        self._solver_timer = QTimer()
        self._solver_timer.timeout.connect(self._poll_solver_output)
        self._solver_timer.start(300)

        output_dir = self._get_result_output_dir()
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.solver_watcher is not None:
            self.solver_watcher.end()
        self.solver_watcher = DirectoryWatcher()
        self.solver_watcher.start(output_dir)
        self.solver_watcher.changed.connect(self.update_solver_file)

    def _read_solver_stdout(self):
        """백그라운드 스레드: solver stdout을 한 줄씩 읽어서 큐에 넣음"""
        try:
            for raw_line in self._solver_proc.stdout:
                if isinstance(raw_line, bytes):
                    line = raw_line.decode('utf-8', errors='replace')
                else:
                    line = raw_line
                self._solver_queue.put(line.rstrip('\n\r'))
        except Exception:
            pass
        self._solver_queue.put(None)  # sentinel: stdout 닫힘

    def _on_output_combo_changed(self, index):
        if index == getattr(self, '_console_combo_index', -1):
            QTimer.singleShot(50, self._restore_console_output)

    def _restore_console_output(self):
        buf = getattr(self, '_solver_output_buf', '')
        if buf:
            self.cmd._output_view.setPlainText(buf)
            scrollbar = self.cmd._output_view.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def _update_solver_output(self, new_text):
        self._solver_output_buf += new_text
        self.cmd._output_view.moveCursor(QTextCursor.MoveOperation.End)
        self.cmd._output_view.insertPlainText(new_text)
        scrollbar = self.cmd._output_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _drain_solver_queue(self):
        """큐에 쌓인 출력 라인을 모두 표시. stdout이 닫혔으면 True 반환"""
        while True:
            try:
                line = self._solver_queue.get_nowait()
            except queue.Empty:
                return False
            if line is None:
                return True
            clean = _ANSI_RE.sub('', line)
            if clean.strip():
                self._update_solver_output(clean + '\n')

    def _poll_solver_output(self):
        if not self._solver_proc:
            self._solver_timer.stop()
            return

        stdout_closed = self._drain_solver_queue()

        # 프로세스 종료 확인
        if self._solver_proc.poll() is not None or stdout_closed:
            self._solver_timer.stop()
            self._drain_solver_queue()  # 남은 출력 drain

            try:
                self._solver_proc.wait(timeout=3)
            except Exception:
                pass
            exit_code = self._solver_proc.returncode
            if exit_code is not None and exit_code == 0:
                self.cmd.add_log_notice('Solver completed')
                self._set_solver_progress(running=False, text='완료', value=100)
            elif exit_code is not None:
                self.cmd.add_log_error(0, f'Solver stopped (exit code: {exit_code})')
                self._set_solver_progress(running=False, text='중지됨', value=0)
            else:
                self.cmd.add_log_notice('Solver finished')
                self._set_solver_progress(running=False, text='완료', value=100)
            self._solver_proc = None
            self.action_run.setEnabled(True)
            self.action_stop.setEnabled(False)
            if self.solver_watcher is not None:
                self.solver_watcher.end()
                self.solver_watcher = None

    def stop_solver(self):
        if getattr(self, '_solver_timer', None):
            self._solver_timer.stop()

        if getattr(self, '_solver_proc', None) and self._solver_proc.poll() is None:
            pid = self._solver_proc.pid
            # 프로세스 트리 강제 종료
            try:
                subprocess.call(
                    ['taskkill', '/F', '/T', '/PID', str(pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                try:
                    self._solver_proc.kill()
                except Exception:
                    pass
            try:
                self._solver_proc.wait(timeout=5)
            except Exception:
                pass
            self._solver_proc = None
            self.cmd.add_log_notice('Solver stopped by user')
            self.action_run.setEnabled(True)
            self.action_stop.setEnabled(False)
            self._set_solver_progress(running=False, text='중지됨', value=0)

        if self.solver_watcher is not None:
            self.solver_watcher.end()
            self.solver_watcher = None

    def _set_solver_progress(self, running, text='', value=0):
        """솔버 진행 상태를 진행바에 표시. 퍼센트를 모르므로 실행 중엔 부정형(계속 움직임)으로
        보여줘서, 로그를 안 봐도 실행 중인지 멈췄는지 한눈에 알 수 있게 한다."""
        pb = getattr(self.cmd, '_progressbar', None)
        if pb is None:
            return
        if running:
            pb.setRange(0, 0)
            pb.setFormat('실행 중...')
        else:
            pb.setRange(0, 100)
            pb.setValue(value)
            pb.setFormat(text)
