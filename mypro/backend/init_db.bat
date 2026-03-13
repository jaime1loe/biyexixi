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
    echo.
    echo 请手动执行SQL文件:
    echo   mysql -u root ^< init_database.sql
    echo.
    echo 或使用MySQL Workbench打开 init_database.sql 执行
    pause
    exit /b 1
)

echo [提示] 正在执行SQL脚本...
echo.

mysql -u root < init_database.sql

if %errorlevel% equ 0 (
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
) else (
    echo.
    echo [错误] 数据库初始化失败
    echo 请检查MySQL是否正常运行以及密码是否正确
)

pause
