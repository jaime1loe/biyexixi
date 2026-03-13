@echo off
chcp 65001 >nul
title 系统启动器
color 0A

echo ============================================================
echo 基于大模型智能体的高校知识库在线答疑系统
echo ============================================================
echo.

echo [步骤 1] 启动后端服务
echo ------------------------------------------------------------
cd /d "%~dp0"

start "后端服务 - 不要关闭" cmd /k "cd /d %~dp0backend && python main.py"

echo 后端服务已启动
echo 等待 8 秒...
timeout /t 8 /nobreak >nul

echo.
echo [步骤 2] 启动前端服务
echo ------------------------------------------------------------
start "前端服务 - 不要关闭" cmd /k "cd /d %~dp0frontend && npm run dev"

echo 前端服务已启动
echo 等待 5 秒...
timeout /t 5 /nobreak >nul

echo.
echo [步骤 3] 打开浏览器
echo ------------------------------------------------------------
start http://localhost:5173

echo.
echo ============================================================
echo 启动完成！
echo ============================================================
echo.
echo 访问地址: http://localhost:5173
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 测试账号:
echo   管理员: admin / admin123
echo   教师:   teacher / 123456
echo   学生:  student1 / 123456
echo.
echo 注意事项:
echo   1. 不要关闭上面打开的两个黑色命令窗口
echo   2. 如需停止，在对应窗口按 Ctrl+C
echo   3. 数据库密码: 20040618
echo.
pause
