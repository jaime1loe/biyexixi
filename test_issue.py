"""
诊断登录问题：数据库连接失败
"""
import os
import sys
import subprocess
import time

print("=== 登录问题诊断 ===\n")

# 1. 检查MySQL服务
print("1. 检查MySQL服务状态...")
try:
    result = subprocess.run(
        ['sc', 'query', 'MySQL'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if "RUNNING" in result.stdout:
        print("   [OK] MySQL服务正在运行")
    else:
        print("   [ERROR] MySQL服务未运行")
        print("   请启动MySQL服务")
except Exception as e:
    print(f"   [WARN] 检查MySQL服务失败: {e}")

print()

# 2. 检查数据库连接
print("2. 检查数据库连接...")
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    # 检查数据库配置
    from app.config import settings
    print(f"   数据库配置:")
    print(f"   主机: {settings.DB_HOST}")
    print(f"   端口: {settings.DB_PORT}")
    print(f"   数据库名: {settings.DB_NAME}")
    print(f"   用户名: {settings.DB_USER}")
    
    # 测试数据库连接
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
        print("   [OK] 数据库连接成功")
        
        # 检查users表
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   users表中有 {user_count} 条记录")
            
            # 检查默认用户
            cursor.execute("SELECT username, role, password FROM users LIMIT 5")
            users = cursor.fetchall()
            print(f"   前5个用户:")
            for user in users:
                print(f"     用户名: {user[0]}, 角色: {user[1]}")
        
        conn.close()
    except pymysql.Error as e:
        print(f"   [ERROR] 数据库连接失败: {e}")
        if "Access denied" in str(e):
            print("     用户名或密码错误")
        elif "Unknown database" in str(e):
            print("     数据库不存在")
        elif "Can't connect" in str(e):
            print("     无法连接到MySQL服务器")
            
except Exception as e:
    print(f"   ✗ 检查数据库失败: {e}")

print()

# 3. 检查后端服务
print("3. 检查后端服务...")
try:
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("   [OK] 后端服务正在运行")
        else:
            print(f"   [ERROR] 后端服务异常，状态码: {response.status_code}")
    except requests.ConnectionError:
        print("   [ERROR] 后端服务未运行")
        print("   请启动后端服务:")
        print("   cd backend && python main.py")
except Exception as e:
    print(f"   [ERROR] 检查后端服务失败: {e}")

print()

# 4. 检查前端服务
print("4. 检查前端服务...")
try:
    import requests
    try:
        response = requests.get("http://localhost:5173", timeout=3)
        if response.status_code == 200:
            print("   [OK] 前端服务正在运行")
        else:
            print(f"   [ERROR] 前端服务异常，状态码: {response.status_code}")
    except requests.ConnectionError:
        print("   [ERROR] 前端服务未运行")
        print("   请启动前端服务:")
        print("   cd frontend && npm run dev")
except Exception as e:
    print(f"   [ERROR] 检查前端服务失败: {e}")

print()

# 5. 总结
print("=== 诊断总结 ===")
print("1. 如果是数据库连接失败:")
print("   - 确保MySQL服务已启动")
print("   - 检查数据库配置 (backend/app/config.py)")
print("   - 确保数据库 'qa_system' 存在")
print("   - 确保用户表 'users' 存在且有数据")

print("\n2. 如果是后端服务未运行:")
print("   - 启动后端服务: cd backend && python main.py")

print("\n3. 如果是前端服务未运行:")
print("   - 启动前端服务: cd frontend && npm run dev")

print("\n4. 如果是账号密码错误:")
print("   - 默认账号:")
print("     管理员: admin / admin123")
print("     学生: student / student123")
print("     教师: teacher / teacher123")
print("   - 如果默认账号无效，检查数据库users表")

print("\n解决方案:")
print("1. 运行 '完整启动系统.bat' 启动所有服务")
print("2. 如果MySQL未运行，请先启动MySQL服务")
print("3. 如果数据库不存在，运行 'create_tables.py' 创建数据库和表")