@echo off
chcp 65001 >nul
echo ============================================
echo 数据库问题自动修复工具
echo ============================================
echo.

echo [1/5] 启动MySQL服务...
net start mysql 2>nul
if errorlevel 1 (
    echo [警告] 无法自动启动MySQL服务
    echo 请手动在服务管理器中启动MySQL
    echo.
    set /p continue="是否继续? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo [OK] MySQL服务已启动
)
echo.

echo [2/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python
    pause
    exit /b 1
)
echo [OK] Python环境正常
echo.

echo [3/5] 检查并创建数据库...
cd /d "%~dp0backend"
python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='12345678'); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.commit(); print('数据库qa_system已就绪')" 2>nul
if errorlevel 1 (
    echo [错误] 无法创建数据库，可能的原因：
    echo   1. MySQL密码不是 12345678
    echo   2. MySQL服务未正常启动
    echo.
    echo 请检查数据库配置: backend/app/config.py
    pause
    exit /b 1
)
echo [OK] 数据库检查通过
echo.

echo [4/5] 检查依赖包...
python -c "import fastapi, pymysql, sqlalchemy" 2>nul
if errorlevel 1 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)
echo [OK] 依赖包完整
echo.

echo [5/5] 检查并修复数据库表结构...
python migrate_all_tables.py >nul 2>&1
python reset_data_auto.py >nul 2>&1
python init_data.py >nul 2>&1
if errorlevel 1 (
    echo [警告] 数据库初始化可能失败，但继续尝试启动
) else (
    echo [OK] 数据库初始化完成
)
echo.

echo ============================================
echo 运行完整检查...
echo ============================================
echo.
python full_test.py

echo.
echo ============================================
echo 修复完成！
echo ============================================
echo.
echo 现在可以运行 启动系统.bat 启动服务
echo.
pause
