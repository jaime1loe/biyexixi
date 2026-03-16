import sys
import os
import time

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

print("=== 数据库连接检查 ===")
print("1. 检查数据库配置...")

try:
    from app.config import settings
    print(f"   数据库主机: {settings.DB_HOST}")
    print(f"   数据库端口: {settings.DB_PORT}")
    print(f"   数据库名称: {settings.DB_NAME}")
    print(f"   数据库用户: {settings.DB_USER}")
    print(f"   数据库密码: {'*' * len(settings.DB_PASSWORD)}")
    print(f"   完整连接URL: {settings.DATABASE_URL[:50]}...")
    
    # 检查数据库驱动
    print("\n2. 检查数据库驱动...")
    try:
        import pymysql
        print(f"   PyMySQL版本: {pymysql.__version__}")
    except ImportError as e:
        print(f"   PyMySQL未安装: {e}")
        
    try:
        import sqlalchemy
        print(f"   SQLAlchemy版本: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"   SQLAlchemy未安装: {e}")
        
    # 测试数据库连接
    print("\n3. 测试数据库连接...")
    from app.database import engine
    
    start_time = time.time()
    try:
        with engine.connect() as conn:
            # 执行简单查询测试连接
            result = conn.execute("SELECT 1")
            test_result = result.scalar()
            
            end_time = time.time()
            connection_time = (end_time - start_time) * 1000
            
            print(f"   [OK] 数据库连接成功!")
            print(f"   连接测试结果: {test_result}")
            print(f"   连接耗时: {connection_time:.2f}ms")
            
            # 检查数据库版本
            print("\n4. 检查数据库信息...")
            try:
                version_result = conn.execute("SELECT VERSION()")
                db_version = version_result.scalar()
                print(f"   数据库版本: {db_version}")
            except Exception as e:
                print(f"   获取版本信息失败: {e}")
                
            # 检查数据库中的表
            print("\n5. 检查数据库表...")
            try:
                # 获取所有表
                tables_result = conn.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA = %s
                """, (settings.DB_NAME,))
                
                tables = [row[0] for row in tables_result]
                print(f"   数据库中共有 {len(tables)} 个表:")
                for table in sorted(tables):
                    print(f"     - {table}")
                    
            except Exception as e:
                print(f"   获取表信息失败: {e}")
                
except Exception as e:
    print(f"   [ERROR] 数据库连接失败: {e}")
    print(f"   错误类型: {type(e).__name__}")
    
    # 提供诊断建议
    print("\n6. 诊断建议:")
    if "Access denied" in str(e):
        print("   [WARN] 用户名或密码错误，请检查数据库配置")
    elif "Unknown database" in str(e):
        print("   [WARN] 数据库不存在，请先创建数据库")
    elif "Can't connect" in str(e):
        print("   [WARN] 无法连接到数据库服务器，请检查:")
        print("     - 数据库服务是否启动")
        print("     - 主机地址是否正确")
        print("     - 防火墙设置")
    elif "No module named" in str(e):
        print("   [WARN] 缺少必要的依赖包，请安装:")
        print("     pip install pymysql sqlalchemy")
    
print("\n=== 检查完成 ===")

# 检查后端服务是否在运行
print("\n7. 检查后端服务状态...")
try:
    import requests
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("   [OK] 后端服务运行正常")
    else:
        print(f"   [WARN] 后端服务异常，状态码: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] 后端服务未运行: {e}")