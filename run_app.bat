@echo off
REM One-click: start the Student Result app for manual testing.
cd /d "%~dp0"
if not exist .venv (
  python -m venv .venv
  call .venv\Scripts\activate.bat
  pip install -q -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)
echo App running at http://127.0.0.1:5000  (login: admin / admin123)
echo Close this window to stop the app.
start "" http://127.0.0.1:5000
python -m app.main
