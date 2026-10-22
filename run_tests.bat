@echo off
REM One-click: set up Python environment, run ALL tests, open the HTML report.
cd /d "%~dp0"
where python >nul 2>nul || (echo Python not found. Install Python 3.10+ from python.org and tick "Add Python to PATH". & pause & exit /b 1)
if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
echo Installing requirements (first run takes a minute)...
pip install -q -r requirements.txt
echo.
echo ===== Running all tests (unit, functional, Selenium UI) =====
pytest --html=report.html --self-contained-html
echo.
echo Test report saved as report.html. Opening it...
start "" report.html
pause
