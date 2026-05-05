@echo off
REM Telemedicine API Documentation Generator - Windows Batch Script
REM Usage: Double-click or run from command prompt

echo.
echo ========================================================================
echo.
echo   TELEMEDICINE API DOCUMENTATION GENERATOR
echo.
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://www.python.org
    echo.
    pause
    exit /b 1
)

echo [*] Python version:
python --version
echo.

REM Run the quick generator
echo [*] Running API documentation generator...
echo.

python quick_generate_docs.py

if errorlevel 1 (
    echo.
    echo [ERROR] Generator failed. Check the output above.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All documentation files generated!
echo.
echo Opening generated documentation...
echo.

REM Try to open HTML file
if exist API_DOCS.html (
    echo [*] Opening API_DOCS.html in default browser...
    start API_DOCS.html
    timeout /t 2 /nobreak
)

REM Open file explorer to show files
echo [*] Opening folder to show generated files...
explorer .

echo.
echo Done! Press any key to close this window...
pause
