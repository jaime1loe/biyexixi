@echo off
echo ========================================
echo 纯手动操作指南
echo ========================================
echo.
echo 请按照以下步骤操作：
echo.
echo 步骤1: 打开CMD窗口
echo   按 Win+R，输入 cmd，按回车
echo.
echo 步骤2: 在CMD中执行（一行一行复制粘贴）：
echo   cd C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend
echo   mysql -u root -p12345678 -e "DROP DATABASE IF EXISTS qa_system;"
echo   mysql -u root -p12345678 < init_database.sql
echo   mysql -u root -p12345678 < init_test_data.sql
echo.
echo 步骤3: 启动后端（新CMD窗口）
echo   start cmd /k "cd C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\backend && python main.py"
echo.
echo 步骤4: 启动前端（新CMD窗口）
echo   start cmd /k "cd C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7\frontend && npm run dev"
echo.
echo 步骤5: 打开浏览器
echo   访问 http://localhost:3000
echo.
echo 步骤6: 登录
echo   Username: student
echo   Password: 123456
echo ========================================
echo.
pause
