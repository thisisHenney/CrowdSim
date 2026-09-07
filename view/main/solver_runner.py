"""솔버(RuntimeSPH2D) 실행/중단 및 콘솔 출력 수집

MainWindowView에 믹스인으로 결합된다. 사용하는 호스트 속성:
self.app_info, self.prj, self.cmd, self.vtk, self.action_run, self.action_stop,
self.solver_watcher, self._anim_reset(), self._load_background_map(),
self.save_input_file(), self.update_solver_file()
"""
import ctypes
import queue
import re
import subprocess
import threading
import time
from ctypes import wintypes
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication

from nextlib.utils.watcher import DirectoryWatcher

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

_STILL_ACTIVE = 259
_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_PROCESS_TERMINATE = 0x0001
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000


def _k32():
    return ctypes.WinDLL('kernel32', use_last_error=True)


def _pid_alive(pid):
    """pid가 아직 살아 있는지. 확인할 수 없으면 죽은 것으로 본다."""
    if not pid:
        return False
    try:
        k = _k32()
        h = k.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not h:
            return False
        try:
            code = wintypes.DWORD()
            if not k.GetExitCodeProcess(h, ctypes.byref(code)):
                return False
            return code.value == _STILL_ACTIVE
        finally:
            k.CloseHandle(h)
    except Exception:
        return False


def _kill_tree(pid, timeout=15.0):
    """솔버 프로세스 트리를 확실히 죽인다. 실제로 사라졌으면 True.

    솔버는 자식 프로세스를 하나 더 띄우므로 `/T`가 필요하고, CUDA 호출 안에
    들어가 있으면 종료가 즉시 이루어지지 않아 확인 후 재시도해야 한다.
    """
    if not _pid_alive(pid):
        return True

    def taskkill():
        try:
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(pid)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            pass

    def terminate():
        try:
            k = _k32()
            h = k.OpenProcess(_PROCESS_TERMINATE, False, int(pid))
            if h:
                k.TerminateProcess(h, 1)
                k.CloseHandle(h)
        except Exception:
            pass

    deadline = time.monotonic() + timeout
    attempt = 0
    while time.monotonic() < deadline:
        taskkill()
        if attempt:
            terminate()
        attempt += 1
        for _ in range(20):
            if not _pid_alive(pid):
                return True
            if QApplication.instance() is not None:
                QApplication.processEvents()  # 기다리는 동안 창이 얼지 않게
            time.sleep(0.1)
    return not _pid_alive(pid)


def _close_job(job):
    """잡 핸들을 닫는다. 파이썬 쪽에서 None으로 지우기만 하면 핸들이 샌다.

    닫는 순간 잡에 남은 프로세스가 종료되므로, 프로세스가 이미 끝난 뒤에만 부를 것.
    """
    if not job:
        return
    try:
        _k32().CloseHandle(job)
    except Exception:
        pass


def _bind_to_job(proc):
    """자식을 Job Object에 묶어, GUI가 죽으면 함께 죽게 한다.

    창을 닫아도 솔버가 고아로 남던 문제의 최종 방어선이다. 잡 핸들을 돌려주며,
    호출자가 이 핸들을 살려 두어야 한다(핸들이 닫히는 순간 자식이 종료된다).
    """
    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [('ReadOperationCount', ctypes.c_ulonglong),
                    ('WriteOperationCount', ctypes.c_ulonglong),
                    ('OtherOperationCount', ctypes.c_ulonglong),
                    ('ReadTransferCount', ctypes.c_ulonglong),
                    ('WriteTransferCount', ctypes.c_ulonglong),
                    ('OtherTransferCount', ctypes.c_ulonglong)]

    class _BASIC(ctypes.Structure):
        _fields_ = [('PerProcessUserTimeLimit', ctypes.c_longlong),
                    ('PerJobUserTimeLimit', ctypes.c_longlong),
                    ('LimitFlags', wintypes.DWORD),
                    ('MinimumWorkingSetSize', ctypes.c_size_t),
                    ('MaximumWorkingSetSize', ctypes.c_size_t),
                    ('ActiveProcessLimit', wintypes.DWORD),
                    ('Affinity', ctypes.c_size_t),
                    ('PriorityClass', wintypes.DWORD),
                    ('SchedulingClass', wintypes.DWORD)]

    class _EXTENDED(ctypes.Structure):
        _fields_ = [('BasicLimitInformation', _BASIC),
                    ('IoInfo', _IO_COUNTERS),
                    ('ProcessMemoryLimit', ctypes.c_size_t),
                    ('JobMemoryLimit', ctypes.c_size_t),
                    ('PeakProcessMemoryUsed', ctypes.c_size_t),
                    ('PeakJobMemoryUsed', ctypes.c_size_t)]

    try:
        k = _k32()
        k.CreateJobObjectW.restype = wintypes.HANDLE
        job = k.CreateJobObjectW(None, None)
        if not job:
            return None
        info = _EXTENDED()
        info.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not k.SetInformationJobObject(job, _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
                                         ctypes.byref(info), ctypes.sizeof(info)):
            k.CloseHandle(job)
            return None
        if not k.AssignProcessToJobObject(job, int(proc._handle)):
            k.CloseHandle(job)
            return None
        return job
    except Exception:
        return None


class SolverRunMixin:
    """솔버 프로세스 실행/중단과 stdout 실시간 표시"""

    def run_solver(self):
        self.save_input_file()
        self.set_dirty(False)
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

        # pid는 따로 들고 있는다. _poll_solver_output이 _solver_proc를 비우고 난
        # 뒤에도 중지/종료가 실제 프로세스를 찾을 수 있어야 한다.
        self._solver_pid = self._solver_proc.pid
        self._solver_job = _bind_to_job(self._solver_proc)

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

        self._drain_solver_queue()

        # 파이프가 닫혔다는 것만으로 끝났다고 보면 안 된다. 예전에는 그렇게 판정해
        # `_solver_proc`을 비워 버렸고, 그 뒤로는 중지 버튼이 조건문에 걸려
        # 아무 일도 하지 않은 채 프로세스가 살아남았다.
        if self._solver_proc.poll() is not None:
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
            self._solver_pid = None
            _close_job(getattr(self, '_solver_job', None))
            self._solver_job = None
            self.action_run.setEnabled(True)
            self.action_stop.setEnabled(False)
            if self.solver_watcher is not None:
                self.solver_watcher.end()
                self.solver_watcher = None

    def solver_is_running(self):
        """솔버 프로세스가 실제로 살아 있는지. `_solver_proc`이 아니라 pid로 본다."""
        return _pid_alive(getattr(self, '_solver_pid', None))

    def stop_solver(self):
        if getattr(self, '_solver_timer', None):
            self._solver_timer.stop()

        pid = getattr(self, '_solver_pid', None)
        if _pid_alive(pid):
            # 종료에 몇 초가 걸릴 수 있으므로(CUDA 호출 중이면 즉시 안 죽는다)
            # 먼저 로그를 남겨 눌린 것이 보이게 한다.
            self.cmd.add_log_notice(f'Stopping solver (pid {pid}) ...')
            QApplication.processEvents()

            killed = _kill_tree(pid)
            if killed:
                self.cmd.add_log_notice('Solver stopped by user')
                self._set_solver_progress(running=False, text='중지됨', value=0)
            else:
                self.cmd.add_log_error(
                    0, f'Solver를 중지하지 못했습니다 (pid {pid}). '
                       f'작업 관리자에서 RuntimeSPH2D.exe를 끝내 주세요.')
                self._set_solver_progress(running=False, text='중지 실패', value=0)
        elif pid:
            self.cmd.add_log_notice('Solver stopped by user')
            self._set_solver_progress(running=False, text='중지됨', value=0)

        self._solver_proc = None
        self._solver_pid = None
        _close_job(getattr(self, '_solver_job', None))
        self._solver_job = None
        self.action_run.setEnabled(True)
        self.action_stop.setEnabled(False)

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
