@echo off
echo 正在清理Python缓存文件...
cd /d %~dp0\backend

echo 删除 __pycache__ 文件夹...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo 删除 .pyc 文件...
del /s /q *.pyc

echo.
echo 缓存清理完成！
echo.
echo 请手动重启后端服务以使DELETE路由生效：
echo 1. 停止当前后端服务（Ctrl+C 或关闭终端窗口）
echo 2. 重新运行后端服务
echo.
echo 或者直接双击以下文件：
echo - backend\运行后端.bat
echo - 完整启动系统.bat
pause
