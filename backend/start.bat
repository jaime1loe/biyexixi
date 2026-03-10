@echo off
chcp 65001 >nul
echo ========================================
echo 启动基于大模型智能体的高校知识库在线答疑系统 - 后端服务
echo ========================================
echo.

REM 检查是否已安装依赖
if not exist "venv" (
    echo [提示] 未检测到虚拟环境，正在创建...
    python -m venv venv
    call venv\Scripts\activate
    echo [提示] 正在安装依赖...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
) else (
    call venv\Scripts\activate
)

REM 检查数据库是否存在
python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password=''); conn.cursor().execute('CREATE DATABASE IF NOT EXISTS qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')" 2>nul

echo [提示] 正在启动服务...
echo.
echo ========================================
echo 服务将在以下地址启动：
echo   API文档: http://localhost:8000/docs
echo   健康检查: http://localhost:8000/health
echo ========================================
echo.

python main.py

pause
