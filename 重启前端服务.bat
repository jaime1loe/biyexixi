@echo off
echo 正在重启前端服务...

echo.
echo 步骤1: 清除 Vite 缓存
if exist "frontend\node_modules\.vite" (
    rmdir /s /q "frontend\node_modules\.vite"
    echo [完成] Vite 缓存已清除
) else (
    echo [跳过] Vite 缓存目录不存在
)

echo.
echo 步骤2: 重启前端服务
echo 请在新终端中执行以下命令:
echo   cd frontend
echo   npm run dev
echo.
echo 或者双击 "完整启动系统.bat" 重新启动整个系统
echo.
pause
