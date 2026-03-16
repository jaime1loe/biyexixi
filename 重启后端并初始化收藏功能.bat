@echo off
echo ========================================
echo 初始化收藏功能并重启后端
echo ========================================
echo.

echo [1/3] 初始化收藏表...
cd backend
python init_favorites_table.py
if errorlevel 1 (
    echo 初始化失败，请检查错误信息
    pause
    exit /b
)
echo.

echo [2/3] 停止现有后端服务...
taskkill /F /IM python.exe 2>nul
echo 后端服务已停止
timeout /t 2 >nul
echo.

echo [3/3] 启动后端服务...
echo 正在启动...
start "后端服务" cmd /k "python main.py"
echo.
echo 后端服务已在新窗口启动
echo API 地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 请在前端测试收藏功能
pause
