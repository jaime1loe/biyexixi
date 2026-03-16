@echo off
REM Simple startup script - ASCII only

echo Starting system...

REM Step 1: Reset database
echo Step 1: Reset database...
C:
cd "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"
mysql -u root -p12345678 -e "DROP DATABASE IF EXISTS qa_system;"
mysql -u root -p12345678 < init_database.sql
mysql -u root -p12345678 < init_test_data.sql
echo Database reset done.

REM Step 2: Start backend
echo Step 2: Start backend...
start cmd /k "cd C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend && python main.py"
timeout /t 10

REM Step 3: Start frontend
echo Step 3: Start frontend...
start cmd /k "cd C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend && npm run dev"
timeout /t 15

REM Step 4: Open browser
echo Step 4: Open browser...
start http://localhost:3000

echo ========================================
echo System started!
echo ========================================
echo Login: student / 123456
echo ========================================
pause
