@echo off
chcp 65001 >nul
echo ========================================
echo 快速初始化数据库
echo ========================================
echo.

REM 检查MySQL是否可用
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到mysql命令，请确保MySQL已安装并添加到PATH环境变量
    pause
    exit /b 1
)

REM 尝试执行SQL（无密码）
echo [提示] 尝试连接MySQL...
mysql -u root < init_database.sql 2>nul

if %errorlevel% equ 0 (
    echo ✓ 数据库初始化成功（无密码）！
    goto :success
)

REM 尝试输入密码
echo [提示] 需要MySQL密码，请输入root用户的密码：
set /p MYSQL_PWD=密码:

echo.
echo [提示] 正在执行SQL脚本...
echo.
mysql -u root --password=%MYSQL_PWD% < init_database.sql

if %errorlevel% equ 0 (
    goto :success
) else (
    echo.
    echo [错误] 数据库初始化失败
    echo 请检查MySQL密码是否正确
    echo.
    echo 或者手动执行: mysql -u root -p ^< init_database.sql
    pause
    exit /b 1
)

:success
echo.
echo ========================================
echo ✓ 数据库初始化成功！
echo ========================================
echo.
echo 已创建以下表:
echo   - users (用户表)
echo   - questions (问题表)
echo   - feedbacks (反馈评价表)
echo   - knowledge (知识库表)
echo   - statistics (统计表)
echo.
echo 数据库: qa_system
echo.
echo 下一步: 运行 python init_data.py 初始化测试数据（可选）
echo.
pause
