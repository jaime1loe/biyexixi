@echo off
chcp 65001 >nul
title 高校知识库智能答疑系统

echo ========================================
echo     高校知识库智能答疑系统 - 一键启动
echo ========================================
echo.

:: 启动后端
echo [1/2] 正在启动后端服务...
start "后端服务" cmd /k "cd /d "%~dp0backend" && python main.py"

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 启动前端
echo [2/2] 正在启动前端服务...
start "前端服务" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo 启动完成！
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:5173
echo ========================================
echo.

:: 等待前端启动
timeout /t 5 /nobreak >nul

:: 打开浏览器并跳转到欢迎页面（可选择登录界面）
start http://localhost:5173/
