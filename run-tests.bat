@echo off
REM ==========================================
REM Automated Test Runner for SauceDemo
REM Python + Playwright Version
REM ==========================================

echo ======================================
echo Automated Testing for SauceDemo.com
echo Python + Playwright
echo ======================================
echo.

REM ตรวจสอบว่ามี virtual environment หรือไม่
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo   playwright install
    pause
    exit /b 1
)

REM เปิดใช้งาน virtual environment
call venv\Scripts\activate.bat

echo Select test option:
echo.
echo 1. Run ALL tests
echo 2. Run ALL tests (with browser visible)
echo 3. Run login tests only
echo 4. Run products tests only
echo 5. Run cart tests only
echo 6. Run checkout tests only
echo 7. Run E2E tests only
echo 8. Run smoke tests only
echo 9. Run example/quick tests
echo 10. Generate HTML report
echo 11. Run tests in parallel (fast)
echo 0. Exit
echo.

set /p choice="Enter your choice (0-11): "

if "%choice%"=="1" (
    echo Running ALL tests...
    pytest -v
    goto end
)

if "%choice%"=="2" (
    echo Running ALL tests with browser visible...
    pytest -v --headed
    goto end
)

if "%choice%"=="3" (
    echo Running login tests only...
    pytest tests/test_login.py -v --headed
    goto end
)

if "%choice%"=="4" (
    echo Running products tests only...
    pytest tests/test_products.py -v --headed
    goto end
)

if "%choice%"=="5" (
    echo Running cart tests only...
    pytest tests/test_cart.py -v --headed
    goto end
)

if "%choice%"=="6" (
    echo Running checkout tests only...
    pytest tests/test_checkout.py -v --headed
    goto end
)

if "%choice%"=="7" (
    echo Running E2E tests only...
    pytest tests/test_e2e_complete_flow.py -v --headed
    goto end
)

if "%choice%"=="8" (
    echo Running smoke tests only...
    pytest -m smoke -v --headed
    goto end
)

if "%choice%"=="9" (
    echo Running example/quick tests...
    pytest tests/test_example_quick.py -v --headed --slowmo=500
    goto end
)

if "%choice%"=="10" (
    echo Generating HTML report...
    pytest --html=report.html --self-contained-html -v
    echo.
    echo Report generated: report.html
    echo Opening report...
    start report.html
    goto end
)

if "%choice%"=="11" (
    echo Running tests in parallel...
    echo Installing pytest-xdist if needed...
    pip install pytest-xdist --quiet
    pytest -n auto -v
    goto end
)

if "%choice%"=="0" (
    echo Exiting...
    goto end
)

echo Invalid choice!
pause
exit /b 1

:end
echo.
echo ======================================
echo Tests completed!
echo ======================================
pause
