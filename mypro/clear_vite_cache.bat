@echo off
echo 正在清除 Vite 缓存...
if exist "frontend\node_modules\.vite" (
    rmdir /s /q "frontend\node_modules\.vite"
    echo Vite 缓存已清除
) else (
    echo Vite 缓存目录不存在
)
echo.
echo 请手动重启前端服务：
echo 1. 关闭当前运行 npm run dev 的终端
echo 2. 运行: cd frontend ^&^& npm run dev
echo.
pause
