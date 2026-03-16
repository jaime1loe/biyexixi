@echo off
chcp 65001 >nul
echo =========================================
echo           系统问题诊断
echo =========================================
echo.

echo 1. 检查前端文件...
if exist "frontend\src\App.vue" (
    echo   [OK] 找到App.vue
) else (
    echo   [ERROR] 找不到App.vue
)

if exist "frontend\package.json" (
    echo   [OK] 找到package.json
) else (
    echo   [ERROR] 找不到package.json
)
echo.

echo 2. 检查后端文件...
if exist "backend\main.py" (
    echo   [OK] 找到main.py
) else (
    echo   [ERROR] 找不到main.py
)
echo.

echo 3. 检查常见问题...
echo   a) 前端服务未启动
echo      解决方案: cd frontend ^&^& npm run dev
echo.
echo   b) 后端服务未启动
echo      解决方案: cd backend ^&^& python main.py
echo.
echo   c) 数据库连接失败
echo      检查MySQL服务是否启动
echo.
echo   d) 端口被占用
echo      检查端口5173和8000是否可用
echo.

echo 4. 快速解决方案:
echo   a) 运行 '完整启动系统.bat'
echo   b) 如果失败，手动启动:
echo      1. 启动MySQL服务
echo      2. cd backend ^&^& python main.py
echo      3. cd frontend ^&^& npm run dev
echo.

echo 5. 检查页面无法打开的可能原因:
echo   a) 前端服务未启动 (http://localhost:5173)
echo   b) 路由配置错误
echo   c) Vue组件编译错误
echo   d) 浏览器缓存问题
echo.

echo =========================================
echo   请按顺序执行以下步骤:
echo   1. 检查前端是否在运行: 访问 http://localhost:5173
echo   2. 检查后端是否在运行: 访问 http://localhost:8000/docs
echo   3. 检查MySQL是否在运行
echo =========================================
echo.
pause