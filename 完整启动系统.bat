@echo off
chcp 65001 >nul
echo ========================================
echo  启动完整系统（后端+前端）
echo ========================================
echo.

echo [1/3] 检查MySQL服务...
tasklist | find /i "mysqld.exe" >nul 2>&1
if errorlevel 1 (
    echo  ✗ MySQL服务未运行，请确保MySQL已启动
    echo.
    echo 启动MySQL后，请重新运行此脚本
    pause
    exit /b 1
) else (
    echo  ✓ MySQL服务已运行
)
echo.

echo [2/3] 启动后端服务...
cd /d "%~dp0backend"
tasklist | find /i "python.exe" >nul 2>&1
if errorlevel 1 (
    echo  正在启动后端服务...
    echo  提示：后端服务将在新窗口中启动
    echo  请关注"后端服务"窗口，查看启动日志和错误信息
    start "后端服务" cmd /k "title 后端服务 - 监听端口8000 && python main.py"
    echo  等待后端服务启动...
    timeout /t 8 /nobreak >nul

    :check_backend
    curl -s http://localhost:8000/api/knowledge/ >nul 2>&1
    if errorlevel 1 (
        echo  后端服务启动中...
        timeout /t 2 /nobreak >nul
        goto check_backend
    )
    echo  ✓ 后端服务已启动
) else (
    echo  ✓ 后端服务已在运行
)
echo.

echo [3/3] 启动前端服务...
cd /d "%~dp0frontend"
tasklist | find /i "node.exe" >nul 2>&1
if errorlevel 1 (
    echo  正在启动前端服务...
    echo  提示：前端服务将在新窗口中启动
    echo  请关注"前端服务"窗口，查看启动日志
    start "前端服务" cmd /k "title 前端服务 - 监听端口5173 && npm run dev"
    echo  等待前端服务启动...
    timeout /t 10 /nobreak >nul

    :check_frontend
    curl -s http://localhost:5173 >nul 2>&1
    if errorlevel 1 (
        echo  前端服务启动中...
        timeout /t 3 /nobreak >nul
        goto check_frontend
    )
    echo  ✓ 前端服务已启动
) else (
    echo  ✓ 前端服务已在运行
)
echo.

echo [4/4] 系统就绪...
echo  系统已准备就绪，即将打开浏览器...
echo.

echo ========================================
echo  系统启动完成！
echo ========================================
echo.
echo  访问地址：
echo    欢迎页面: http://localhost:5173/
echo    学生/教师登录: http://localhost:5173/login
echo    管理员登录: http://localhost:5173/admin/login
echo    后端API: http://localhost:8000
echo    API文档: http://localhost:8000/docs
echo.
echo  默认登录账号：
echo    管理员: admin / admin123
echo    学生:   student / student123
echo.
echo  系统说明：
echo    - 双击启动后，会自动打开欢迎页面
echo    - 在欢迎页面选择：学生/教师 或 管理员
echo    - 根据选择进入不同的登录页面
echo    - 后端和前端服务窗口请勿关闭
echo    - 关闭窗口即关闭服务
echo.
timeout /t 2 /nobreak >nul
start http://localhost:5173/

echo.
echo 按任意键关闭此窗口（不影响服务运行）...
pause >nul
