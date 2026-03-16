@echo off
chcp 65001 >nul
echo ================================
echo   系统状态快速检查
echo ================================
echo.

echo 1. 检查MySQL服务...
sc query MySQL | findstr /c:"RUNNING" >nul
if %errorlevel% equ 0 (
    echo   [OK] MySQL服务正在运行
) else (
    echo   [ERROR] MySQL服务未运行
)
echo.

echo 2. 检查端口状态...
echo   端口8000（后端）:
netstat -an | findstr /c:":8000" >nul
if %errorlevel% equ 0 (
    echo     [OK] 端口8000被占用
) else (
    echo     [ERROR] 端口8000空闲
)

echo   端口5173（前端）:
netstat -an | findstr /c:":5173" >nul
if %errorlevel% equ 0 (
    echo     [OK] 端口5173被占用
) else (
    echo     [ERROR] 端口5173空闲
)
echo.

echo 3. 检查数据库连接...
python -c "
import sys
import os
sys.path.append(r'd:\毕业设计\backend')
try:
    from app.config import settings
    print('数据库配置:')
    print('主机: {0}'.format(settings.DB_HOST))
    print('端口: {0}'.format(settings.DB_PORT))
    print('数据库: {0}'.format(settings.DB_NAME))
    print('用户: {0}'.format(settings.DB_USER))
    
    import pymysql
    try:
        conn = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            connect_timeout=5
        )
        print('[OK] 数据库连接成功')
        
        with conn.cursor() as cursor:
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            print('数据库中有 {0} 个表'.format(len(tables)))
            
            if 'users' in [t[0] for t in tables]:
                cursor.execute('SELECT COUNT(*) FROM users')
                user_count = cursor.fetchone()[0]
                print('users表: {0} 条记录'.format(user_count))
            else:
                print('[ERROR] users表不存在')
            
        conn.close()
    except pymysql.Error as e:
        print('[ERROR] 数据库连接失败: {0}'.format(e))
        
except Exception as e:
    print('[ERROR] 检查数据库配置失败: {0}'.format(e))
"
echo.

echo 4. 尝试启动后端服务...
echo  启动命令: python backend/main.py
echo  如果后端未运行，请手动运行上述命令
echo.

echo 5. 尝试启动前端服务...
echo  启动命令: cd frontend ^&^& npm run dev
echo  如果前端未运行，请手动运行上述命令
echo.

echo ================================
echo   建议操作：
echo   1. 确保MySQL服务已启动
echo   2. 启动后端服务
echo   3. 启动前端服务
echo   4. 重新访问登录页面
echo ================================
pause