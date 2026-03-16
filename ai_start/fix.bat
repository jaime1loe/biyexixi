@echo off
REM Fix login issue

echo Fixing login issue...

C:
cd "C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend"

REM Fix password for student
mysql -u root -p12345678 -e "USE qa_system; UPDATE users SET password_hash='\$5\$rounds=535000\$Xkg4VvIF5yTX9WFx\$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8' WHERE username='student';"

REM Verify fix
mysql -u root -p12345678 -e "USE qa_system; SELECT id, username FROM users;"

echo Fix applied. Please restart backend and refresh browser.
pause
