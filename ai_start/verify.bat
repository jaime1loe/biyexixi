@echo off
echo Verifying paths...
echo.

echo Checking backend...
if exist "C:\Users\1\Desktop\*\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\main.py" (
    echo ERROR: Path contains wildcard characters
    echo Your system cannot handle UTF-8 encoding correctly
    echo Please follow the manual instructions instead
    pause
    exit /b 1
)

if exist "C:\Users\1\Desktop\??????\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\main.py" (
    echo ERROR: Encoding issue detected
    echo Please use manual operation method
    pause
    exit /b 1
)

if exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\main.py" (
    echo [OK] Backend found
) else (
    echo [ERROR] Backend NOT found
    echo Please check the actual path
    echo Expected: C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend
    pause
    exit /b 1
)

echo.
echo Checking frontend...
if exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend\package.json" (
    echo [OK] Frontend found
) else (
    echo [ERROR] Frontend NOT found
    pause
    exit /b 1
)

echo.
echo All paths verified successfully!
pause
