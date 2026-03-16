@echo off
echo ========================================
echo  检查前后端连接状态
echo ========================================
echo.

REM 检查后端端口8000
echo 检查后端API (端口8000)...
netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo [ERROR] 后端服务未运行
    echo 请启动后端服务: backend-start.bat
) else (
    echo [OK] 后端服务正在运行
)

REM 检查前端端口3000
echo.
echo 检查前端服务 (端口3000)...
netstat -ano | findstr :3000 >nul
if errorlevel 1 (
    echo [ERROR] 前端服务未运行
    echo 请启动前端服务: frontend-start.bat
) else (
    echo [OK] 前端服务正在运行
)

REM 测试后端API
echo.
echo 测试后端API...
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 无法访问后端API
    echo 请检查后端服务是否启动完成
) else (
    echo [OK] 后端API可访问
)

echo.
echo ========================================
echo 测试登录API
echo ========================================
echo.
echo 使用测试账号登录 (student/123456):
curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d "{""username"":""student"",""password"":""123456""}" -w "\nHTTP状态: %{http_code}\n" -s

echo.
echo ========================================
echo 诊断建议
echo ========================================
echo.
echo 如果登录失败：
echo 1. 确认后端显示: Application startup complete
echo 2. 确认前端显示: ready
echo 3. 刷新浏览器页面 (Ctrl+F5)
echo 4. 检查数据库密码是否正确
echo.
pause
