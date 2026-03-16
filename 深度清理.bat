@echo off
echo ========================================
echo 深度清理 - 释放更多空间
echo ========================================
echo.
echo 警告: 此操作将删除虚拟环境和依赖包
echo 删除后需要重新安装依赖
echo.
set /p confirm="确认执行深度清理？(y/n): "
if /i not "%confirm%"=="y" (
    echo 已取消
    pause
    exit /b
)

echo.
echo [1/2] 删除 Python 虚拟环境...
if exist "backend\venv" (
    rmdir /s /q "backend\venv"
    echo 已删除 backend\venv
)
echo.

echo [2/2] 删除前端 node_modules...
if exist "frontend\node_modules" (
    rmdir /s /q "frontend\node_modules"
    echo 已删除 frontend\node_modules
)
echo.

echo ========================================
echo 深度清理完成！
echo ========================================
echo.
echo 重新安装依赖的步骤:
echo.
echo 1. 后端:
echo    cd backend
echo    python -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo.
echo 2. 前端:
echo    cd frontend
echo    npm install
echo.
pause
