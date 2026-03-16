@echo off
echo ========================================
echo  测试登录功能
echo ========================================
echo.

echo Testing login with student/123456...
curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d "{""username"":""student"",""password"":""123456""}" -w "\nHTTP Status: %{http_code}\n" -s

echo.
echo.
echo Testing login with admin/123456...
curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d "{""username"":""admin"",""password"":""123456""}" -w "\nHTTP Status: %{http_code}\n" -s

echo.
echo.
echo If you see HTTP Status: 200, login is successful
echo If you see HTTP Status: 401, password is incorrect
echo.
pause
