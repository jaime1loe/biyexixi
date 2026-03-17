@echo off
chcp 65001 >nul
title 安装APScheduler依赖
color 0B

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              安装定时任务依赖 (APScheduler)             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0backend"

REM 检查虚拟环境是否存在
if not exist "venv\" (
    echo [信息] 未找到虚拟环境，正在创建...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成
)

REM 激活虚拟环境
call venv\Scripts\activate

echo [1/2] 正在安装 APScheduler...
pip install apscheduler>=3.10.0
if errorlevel 1 (
    echo [错误] 安装失败
    pause
    exit /b 1
)
echo [成功] APScheduler 安装完成
echo.

echo [2/2] 正在更新其他依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 部分依赖更新可能失败，但APScheduler已安装
) else (
    echo [成功] 所有依赖更新完成
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║                    依赖安装完成！                           ║
echo ║                                                           ║
echo ║  APScheduler 已安装，定时发布功能现已可用             ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo [提示] 现在可以启动后端服务
echo.
pause
