Write-Host "=== 系统状态检查 ===" -ForegroundColor Cyan
Write-Host ""

# 1. 检查MySQL服务
Write-Host "1. 检查MySQL服务..." -ForegroundColor Yellow
$mysqlService = Get-Service -Name MySQL -ErrorAction SilentlyContinue
if ($mysqlService) {
    if ($mysqlService.Status -eq 'Running') {
        Write-Host "   [OK] MySQL服务正在运行" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] MySQL服务未运行" -ForegroundColor Red
    }
} else {
    Write-Host "   [WARNING] MySQL服务未找到" -ForegroundColor Yellow
}

Write-Host ""

# 2. 检查数据库连接
Write-Host "2. 检查数据库连接..." -ForegroundColor Yellow
try {
    # 导入Python模块
    $pythonPath = "d:\毕业设计\backend"
    $env:PYTHONPATH = $pythonPath
    
    $pythonCode = @"
import sys
import os
sys.path.append(r'd:\毕业设计\backend')
try:
    from app.config import settings
    print(f"数据库配置:")
    print(f"主机: {settings.DB_HOST}")
    print(f"端口: {settings.DB_PORT}")
    print(f"数据库: {settings.DB_NAME}")
    print(f"用户: {settings.DB_USER}")
    
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
        print("[OK] 数据库连接成功")
        
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"数据库中有 {len(tables)} 个表")
            
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"users表: {user_count} 条记录")
            
        conn.close()
    except pymysql.Error as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        
except Exception as e:
    print(f"[ERROR] 检查数据库配置失败: {e}")
"@
    
    python -c $pythonCode
} catch {
    Write-Host "   [ERROR] 运行Python检查失败" -ForegroundColor Red
}

Write-Host ""

# 3. 检查后端服务
Write-Host "3. 检查后端服务 (端口8000)..." -ForegroundColor Yellow
$port8000 = netstat -an | findstr ":8000"
if ($port8000) {
    Write-Host "   [OK] 后端服务端口8000被占用" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] 后端服务未运行" -ForegroundColor Red
}

Write-Host ""

# 4. 检查前端服务
Write-Host "4. 检查前端服务 (端口5173)..." -ForegroundColor Yellow
$port5173 = netstat -an | findstr ":5173"
if ($port5173) {
    Write-Host "   [OK] 前端服务端口5173被占用" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] 前端服务未运行" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== 解决方案 ===" -ForegroundColor Cyan
Write-Host "1. 如果MySQL未运行:" -ForegroundColor Yellow
Write-Host "   - 启动MySQL服务" -ForegroundColor White
Write-Host ""
Write-Host "2. 如果后端服务未运行:" -ForegroundColor Yellow
Write-Host "   - cd backend" -ForegroundColor White
Write-Host "   - python main.py" -ForegroundColor White
Write-Host ""
Write-Host "3. 如果前端服务未运行:" -ForegroundColor Yellow
Write-Host "   - cd frontend" -ForegroundColor White
Write-Host "   - npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "4. 如果数据库连接失败:" -ForegroundColor Yellow
Write-Host "   - 检查backend/app/config.py中的数据库配置" -ForegroundColor White
Write-Host "   - 确保MySQL中有qa_system数据库" -ForegroundColor White
Write-Host ""
Write-Host "5. 快速启动完整系统:" -ForegroundColor Yellow
Write-Host "   - 运行 '完整启动系统.bat'" -ForegroundColor White