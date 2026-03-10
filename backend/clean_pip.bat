@echo off
chcp 65001 >nul
echo ========================================
echo Cleaning pip cache and requirements
echo ========================================
echo.

echo [1/3] Clearing pip cache...
pip cache purge
echo.

echo [2/3] Uninstalling existing packages...
pip uninstall -y fastapi uvicorn sqlalchemy pymysql pydantic passlib python-jose python-multipart aiofiles
echo.

echo [3/3] Installing fresh dependencies...
pip install -r requirements-core.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo Done!
echo ========================================
pause
