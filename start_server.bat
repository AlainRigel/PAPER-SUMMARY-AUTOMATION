@echo off
echo ========================================
echo   Paper Collector - Web Interface
echo   Academic Research Cognitive Amplifier
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found.
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [+] Virtual environment created.
    echo.
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo [*] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies not installed.
    echo [*] Installing dependencies...
    pip install -r requirements.txt
    echo [+] Dependencies installed.
    echo.
)

REM Start the server
echo [*] Starting Paper Collector server...
echo.
echo ========================================
echo   Server will start at:
echo   http://localhost:8000
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
