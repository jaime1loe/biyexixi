@echo off
chcp 65001 >nul
echo ============================================
echo 前端问题修复脚本
echo ============================================
echo.
echo [1/5] 清除前端缓存...
cd /d "%~dp0frontend"

if exist "dist" (
    echo 删除dist目录...
    rmdir /s /q dist
)

if exist "node_modules\.vite" (
    echo 删除Vite缓存...
    rmdir /s /q node_modules\.vite
)

echo.
echo [2/5] 检查依赖...
if not exist "node_modules" (
    echo 正在安装依赖...
    call npm install --registry=https://registry.npmmirror.com
)

echo.
echo [3/5] 重新启动前端服务...
echo 前端服务将在 http://localhost:5173 启动
echo.
start "前端服务" cmd /k "chcp 65001 >nul && npm run dev"

echo.
echo [4/5] 等待服务启动...
timeout /t 8 /nobreak >nul

echo.
echo [5/5] 自动打开浏览器...
start http://localhost:5173

echo.
echo ============================================
echo 修复完成！
echo ============================================
echo.
echo 如果页面仍有问题，请按以下步骤操作：
echo   1. 在浏览器中按 Ctrl+Shift+Delete 清除缓存
echo   2. 按 Ctrl+F5 强制刷新页面（或 Ctrl+Shift+R）
echo   3. 关闭前端窗口，重新运行此脚本
echo   4. 如果问题依旧，请查看相关文档
echo.
pause
