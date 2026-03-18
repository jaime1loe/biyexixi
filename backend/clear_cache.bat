@echo off
echo Clearing Python cache...
if exist __pycache__ rd /s /q __pycache__
if exist app\__pycache__ rd /s /q app\__pycache__
if exist app\routers\__pycache__ rd /s /q app\routers\__pycache__
if exist app\schemas.py del /f app\schemas.py 2>NUL
if exist app\*.pyc del /f /q app\*.pyc 2>NUL
echo Cache cleared.
echo.
echo Please restart the backend server manually or run restart_server.bat
pause
