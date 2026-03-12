@echo off
chcp 65001 >nul
title 前端服务 - QA System Frontend
color 0B

cd /d "%~dp0"

echo ============================================================
echo 启动前端服务
echo ============================================================
echo.

echo 检查依赖...
if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install --registry=https://registry.npmmirror.com
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 启动开发服务器...
echo.
echo 服务信息:
echo   地址: http://localhost:5173
echo.
echo 正在启动服务器...
echo 按 Ctrl+C 可以停止服务
echo.
echo ============================================================
echo.

npm run dev

pause
