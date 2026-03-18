@echo off
echo 正在停止Python进程...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo 清理缓存...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo 完成！
