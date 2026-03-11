@echo off
chcp 65001 >nul
echo ========================================
echo Installing core dependencies
echo ========================================
echo.

pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings passlib[bcrypt] python-jose[cryptography] python-multipart aiofiles -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo Next steps:
echo 1. Run init_db_with_pwd.bat to create database
echo 2. Run python main.py to start the server
echo.
pause
