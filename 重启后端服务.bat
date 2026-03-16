@echo off
chcp 65001 >nul
echo ========================================
echo  重启后端服务
echo ========================================
echo.
echo 正在停止现有的Python进程...

tasklist | find /i "python.exe" >nul 2>&1
if not errorlevel 1 (
    echo  检测到运行中的Python进程，正在停止...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo  ✓ 已停止所有Python进程
) else (
    echo  ✓ 没有运行中的Python进程
)
echo.

echo 正在清理Python缓存...
cd /d "%~dp0backend\app"
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo  ✓ 缓存清理完成
echo.

echo 正在启动后端服务...
echo.
echo ========================================
echo  后端服务将在下方窗口中启动
echo  请关注启动日志和可能的错误信息
echo  窗口标题: 后端服务 - 实时日志
echo ========================================
echo.
cd /d "%~dp0backend"
start "后端服务 - 实时日志" cmd /k "title 后端服务 - 实时日志 - 端口8000 && python main.py"

echo.
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 检查后端服务状态...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo  ✗ 后端服务启动失败或还在启动中
    echo  请查看"后端服务 - 实时日志"窗口中的错误信息
    echo.
    echo 常见问题：
    echo  1. 数据库连接失败 - 检查MySQL服务是否启动
    echo  2. 端口被占用 - 检查8000端口是否被其他程序占用
    echo  3. 依赖缺失 - 运行 pip install -r requirements.txt
) else (
    echo  ✓ 后端服务启动成功！
    echo  ✓ 健康检查通过
)
echo.
echo 后端API地址：http://localhost:8000
echo API文档地址：http://localhost:8000/docs
echo.
pause
