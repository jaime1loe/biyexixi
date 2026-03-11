@echo off
chcp 65001 >nul
echo ============================================
echo 基于大模型智能体的高校知识库在线答疑系统
echo 一键启动脚本
echo ============================================
echo.

echo [1/3] 检查后端环境...
cd /d "%~dp0backend"

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 检查依赖包...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [提示] 正在安装后端依赖...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo 检查数据库连接...
python -c "import sys; sys.path.insert(0, '.'); from app.config import settings; print('Database:', settings.DB_NAME)" 2>nul
if errorlevel 1 (
    echo [提示] 请确保MySQL服务已启动，且密码为12345678
    pause
    exit /b 1
)

echo.
echo [2/3] 启动后端服务...
echo 后端服务将在 http://localhost:8000 启动
echo API文档地址: http://localhost:8000/docs
echo.
start "后端服务" cmd /k "python main.py"

echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] 启动前端服务...
cd /d "%~dp0frontend"

echo 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Node.js，请先安装Node.js
    echo [提示] 访问 https://nodejs.org/ 下载LTS版本
    pause
    exit /b 1
)

echo 检查前端依赖...
if not exist "node_modules" (
    echo [提示] 正在安装前端依赖（首次运行需要几分钟）...
    call npm install --registry=https://registry.npmmirror.com
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)

echo 前端服务将在 http://localhost:5173 启动
echo [提示] 如果出现乱码，请按Ctrl+C停止后重新运行此脚本
echo.
start "前端服务" cmd /k "chcp 65001 >nul && npm run dev"

echo.
echo 等待前端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo ============================================
echo 启动完成！正在打开浏览器...
echo ============================================
echo.

start http://localhost:5173

echo 系统信息：
echo   前端界面: http://localhost:5173
echo   后端API:  http://localhost:8000
echo   API文档:  http://localhost:8000/docs
echo.
echo 测试账号：
echo   管理员: admin / admin123
echo   教师:   teacher / 123456
echo   学生1:  student1 / 123456
echo   学生2:  student2 / 123456
echo.
echo 注意事项：
echo   1. 不要关闭上述两个命令窗口
echo   2. 如需停止，请在对应窗口按 Ctrl+C
echo   3. 数据库密码: 12345678
echo   4. 如果浏览器未自动打开，请手动访问 http://localhost:5173
echo.
pause
