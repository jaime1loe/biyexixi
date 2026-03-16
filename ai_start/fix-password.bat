@echo off
echo Fixing password issue...
echo.

C:
cd "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"

echo Step 1: Delete database...
mysql -u root -p12345678 -e "DROP DATABASE IF EXISTS qa_system;"

echo Step 2: Create database...
mysql -u root -p12345678 < init_database.sql

echo Step 3: Insert test data...
mysql -u root -p12345678 < init_test_data.sql

echo Step 4: Verify users...
mysql -u root -p12345678 -e "USE qa_system; SELECT id, username, real_name FROM users;"

echo.
echo Database reset complete!
echo All passwords are now: 123456
echo.
echo Next steps:
echo 1. Restart backend service
echo 2. Refresh browser (Ctrl+F5)
echo 3. Login with: student / 123456
echo.
pause
