@echo off
echo Testing password verification...
echo.

C:
cd "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"

REM Check current password hash in database
echo Current password hash in database:
mysql -u root -p12345678 -e "USE qa_system; SELECT id, username, password_hash FROM users WHERE username='student';"

REM Test login with SQL
echo.
echo Testing login with SQL:
mysql -u root -p12345678 -e "USE qa_system; SELECT id, username, real_name FROM users WHERE username='student' AND password_hash='\$5\$rounds=535000\$Xkg4VvIF5yTX9WFx\$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8';"

pause
