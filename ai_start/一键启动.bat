@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    Intelligent Q&A System Starter
echo ========================================
echo.

set "PROJECT_DIR=C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7"
set "BACKEND_DIR=%PROJECT_DIR%\backend"
set "FRONTEND_DIR=%PROJECT_DIR%\frontend"

echo [1/5] Checking MySQL service...
net start | findstr /i "mysql" >nul
if %ERRORLEVEL% NEQ 0 (
    net start mysql8 >nul 2>&1
)
echo [OK] MySQL is running

echo.
echo [2/5] Starting Backend server...
start "Backend Server" cmd /k "cd /d "%BACKEND_DIR%" && python main.py"
echo [OK] Backend starting on http://localhost:8000

echo.
echo [3/5] Checking npm dependencies...
if not exist "%FRONTEND_DIR%\node_modules" (
    echo     Installing npm packages...
    cd /d "%FRONTEND_DIR%"
    call npm install
)
echo [OK] Dependencies ready

echo.
echo [4/5] Starting Frontend server...
start "Frontend Server" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"
echo [OK] Frontend starting on http://localhost:3000

echo.
echo [5/5] Waiting for services to be ready...
timeout /t 8 /nobreak >nul

echo.
echo ========================================
echo    All services started successfully!
echo ========================================
echo.
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:3000
echo.
echo    Login credentials:
echo      Student: student / 123456
echo      Admin: admin / 123456
echo.
echo Opening browser...
start http://localhost:3000

echo.
echo Press any key to exit this window...
pause >nul
