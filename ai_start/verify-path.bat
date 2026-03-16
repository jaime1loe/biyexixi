@echo off
echo Verifying paths...
echo.

if exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\main.py" (
    echo [OK] Backend path exists
) else (
    echo [ERROR] Backend path NOT found
    echo Path: C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend
)

if exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend\package.json" (
    echo [OK] Frontend path exists
) else (
    echo [ERROR] Frontend path NOT found
    echo Path: C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend
)

pause
