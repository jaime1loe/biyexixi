@echo off
echo Starting system...
echo.

REM Use pushd to handle paths with special characters

REM Step 1: Reset database
echo Step 1: Reset database...
pushd "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"
mysql -u root -p12345678 -e "DROP DATABASE IF EXISTS qa_system;"
mysql -u root -p12345678 < init_database.sql
mysql -u root -p12345678 < init_test_data.sql
popd
echo Database reset done.
echo.

REM Step 2: Start backend
echo Step 2: Start backend...
start "Backend" cmd /k "pushd \"C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend\" && python main.py"
timeout /t 10
echo Backend started.
echo.

REM Step 3: Start frontend
echo Step 3: Start frontend...
start "Frontend" cmd /k "pushd \"C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend\" && npm run dev"
timeout /t 15
echo Frontend started.
echo.

REM Step 4: Open browser
echo Step 4: Open browser...
start http://localhost:3000

echo ========================================
echo System started successfully!
echo ========================================
echo.
echo Login Info:
echo   Username: student
echo   Password: 123456
echo.
echo Please wait for the page to load, then login.
echo ========================================
pause
