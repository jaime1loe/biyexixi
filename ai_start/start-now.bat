@echo off
REM Force UTF-8 encoding
chcp 65001 >nul

echo ========================================
echo  System Startup - Login System
echo ========================================
echo.

REM Check if backend path exists
echo Checking backend path...
if not exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\main.py" (
    echo ERROR: Backend path not found
    echo Please check the path: C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend
    echo.
    echo If you see garbled characters, your system has encoding issues.
    echo Please follow manual instructions instead.
    pause
    exit /b 1
)

echo Backend path OK
echo.

REM Check if frontend path exists
echo Checking frontend path...
if not exist "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend\package.json" (
    echo ERROR: Frontend path not found
    pause
    exit /b 1
)

echo Frontend path OK
echo.

REM Step 1: Reset database
echo Step 1: Reset database...
cd /d "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"
mysql -u root -p12345678 -e "DROP DATABASE IF EXISTS qa_system;"
mysql -u root -p12345678 < init_database.sql
mysql -u root -p12345678 < init_test_data.sql
echo Database reset done.
echo.

REM Step 2: Fix password (IMPORTANT!)
echo Step 2: Fix password for login...
mysql -u root -p12345678 -e "USE qa_system; UPDATE users SET password_hash='\$5\$rounds=535000\$Xkg4VvIF5yTX9WFx\$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8' WHERE username='student';"
mysql -u root -p12345678 -e "USE qa_system; UPDATE users SET password_hash='\$5\$rounds=535000\$Xkg4VvIF5yTX9WFx\$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8' WHERE username='admin';"
mysql -u root -p12345678 -e "USE qa_system; UPDATE users SET password_hash='\$5\$rounds=535000\$Xkg4VvIF5yTX9WFx\$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8' WHERE username='teacher';"
echo Password fixed.
echo.

REM Step 3: Start backend
echo Step 3: Start backend service...
start "Backend" cmd /k "cd /d C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend && python main.py"
timeout /t 15
echo Backend started.
echo.

REM Step 4: Start frontend
echo Step 4: Start frontend service...
start "Frontend" cmd /k "cd /d C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend && npm run dev"
timeout /t 20
echo Frontend started.
echo.

REM Step 5: Open browser
echo Step 5: Open browser...
start http://localhost:3000

echo ========================================
echo System startup complete!
echo ========================================
echo.
echo Login Information:
echo   Username: student
echo   Password: 123456
echo.
echo Steps:
echo 1. Wait for browser to open
echo 2. Enter username and password
echo 3. Click Login button
echo 4. You will be redirected to homepage
echo ========================================
pause
