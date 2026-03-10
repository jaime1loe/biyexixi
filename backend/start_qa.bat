@echo off
chcp 65001 >nul
echo ========================================
echo Quick Start Guide
echo ========================================
echo.
echo Checking dependencies...

python -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [!] Dependencies not installed
    echo [1] Running install_deps.bat...
    call install_deps.bat
) else (
    echo [✓] Dependencies installed
)

echo.
echo ========================================
echo Starting backend server...
echo ========================================
echo.
echo Server will be available at:
echo   - API Docs: http://localhost:8000/docs
echo   - Health:   http://localhost:8000/health
echo.
echo Press Ctrl+C to stop
echo.

python main.py
