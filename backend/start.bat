@echo off
echo Starting FastAPI Backend Server...

REM 检查虚拟环境
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo Installing dependencies...
pip install -r requirements.txt

REM 启动服务
echo Starting server...
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
