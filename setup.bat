@echo off
REM ==========================================
REM Setup Script for SauceDemo Automated Tests
REM Python + Playwright Version
REM ==========================================

echo ======================================
echo Setup - Automated Testing
echo Python + Playwright
echo ======================================
echo.

REM ตรวจสอบ Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)
python --version
echo [OK] Python is installed
echo.

REM สร้าง Virtual Environment
echo [2/5] Creating virtual environment...
if exist "venv" (
    echo [SKIP] Virtual environment already exists
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM เปิดใช้งาน Virtual Environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM ติดตั้ง Dependencies
echo [4/5] Installing Python dependencies...
echo This may take a few minutes...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM ติดตั้ง Playwright Browsers
echo [5/5] Installing Playwright browsers...
echo This may take 5-10 minutes...
playwright install
if errorlevel 1 (
    echo [ERROR] Failed to install Playwright browsers
    pause
    exit /b 1
)
echo [OK] Playwright browsers installed
echo.

REM สร้างโฟลเดอร์สำหรับ screenshots
if not exist "screenshots" (
    mkdir screenshots
    echo [OK] Created screenshots folder
)

echo ======================================
echo Setup completed successfully!
echo ======================================
echo.
echo You can now run tests using:
echo   1. run-tests.bat (menu-based)
echo   2. pytest -v (command line)
echo.
echo Quick start:
echo   venv\Scripts\activate
echo   pytest tests/test_example_quick.py -v --headed
echo.
pause
