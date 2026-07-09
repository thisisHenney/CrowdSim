@echo off
rem CrowdSim 실행 (프로젝트 가상환경 사용)
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv 가 없습니다. 먼저 생성하세요:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
".venv\Scripts\python.exe" main.py %*
