@echo off
chcp 65001 >nul
echo ============================================
echo 初始化数据库
echo ============================================
echo.

cd /d "%~dp0backend"

echo [1/2] 创建数据库...
python -c "import pymysql; conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678'); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); print('数据库创建成功'); conn.commit(); cursor.close(); conn.close()" 2>&1

if errorlevel 1 (
    echo [错误] 数据库创建失败！
    echo 请检查：
    echo   1. MySQL服务是否已启动
    echo   2. MySQL密码是否为 12345678
    echo   3. 是否有创建数据库的权限
    pause
    exit /b 1
)

echo.
echo [2/2] 初始化数据表...
python init_data.py

if errorlevel 1 (
    echo [错误] 数据表初始化失败！
    pause
    exit /b 1
)

echo.
echo ============================================
echo 数据库初始化完成！
echo ============================================
echo.
pause
