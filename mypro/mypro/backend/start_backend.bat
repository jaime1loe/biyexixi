@echo off
chcp 65001 >nul
title 后端服务 - QA System Backend
color 0A

cd /d "%~dp0"

echo ============================================================
echo 启动后端服务
echo ============================================================
echo.

echo [1/2] 测试数据库连接...
python test_db_connection.py
if errorlevel 1 (
    echo.
    echo [错误] 数据库连接失败！
    pause
    exit /b 1
)

echo.
echo [2/2] 启动服务器...
echo.
echo 服务信息:
echo   地址: http://localhost:8000
echo   文档: http://localhost:8000/docs
echo.
echo 正在启动服务器...
echo 按 Ctrl+C 可以停止服务
echo.
echo ============================================================
echo.

python main.py

pause
