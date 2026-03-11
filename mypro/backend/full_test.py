"""
完整启动前检查脚本
"""
import sys
import pymysql

print("=" * 60)
print("系统启动前完整检查")
print("=" * 60)

# 检查1: pymysql模块
print("\n[1/5] 检查pymysql模块...")
try:
    import pymysql
    print(f"  OK - pymysql版本: {pymysql.__version__}")
except ImportError:
    print("  FAIL - pymysql未安装")
    print("  解决方案: pip install pymysql")
    sys.exit(1)

# 检查2: MySQL服务器连接
print("\n[2/5] 检查MySQL服务器...")
try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        connect_timeout=5
    )
    print("  OK - MySQL服务器连接成功")
    conn.close()
except Exception as e:
    print(f"  FAIL - {e}")
    print("  解决方案:")
    print("    1. 启动MySQL服务: net start mysql")
    print("    2. 检查密码是否为: 12345678")
    sys.exit(1)

# 检查3: 数据库存在
print("\n[3/5] 检查数据库qa_system...")
try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        database='qa_system',
        connect_timeout=5
    )
    print("  OK - 数据库qa_system存在")
    conn.close()
except Exception as e:
    if "Unknown database" in str(e):
        print("  FAIL - 数据库qa_system不存在")
        print("  解决方案: CREATE DATABASE qa_system CHARACTER SET utf8mb4;")
    else:
        print(f"  FAIL - {e}")
    sys.exit(1)

# 检查4: 数据表存在
print("\n[4/5] 检查数据表...")
try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        database='qa_system'
    )
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')
    tables = [t[0] for t in cursor.fetchall()]

    expected_tables = ['users', 'questions', 'feedbacks', 'knowledge', 'statistics']
    missing = [t for t in expected_tables if t not in tables]

    if missing:
        print(f"  FAIL - 缺少表: {', '.join(missing)}")
        print("  解决方案: 运行初始化脚本")
        conn.close()
        sys.exit(1)
    else:
        print(f"  OK - 所有必需的表都已创建")
        for t in tables:
            print(f"    - {t}")

    conn.close()
except Exception as e:
    print(f"  FAIL - {e}")
    sys.exit(1)

# 检查5: 应用配置加载
print("\n[5/5] 检查应用配置...")
try:
    sys.path.insert(0, '.')
    from app.config import settings
    print(f"  OK - 配置加载成功")
    print(f"    数据库URL: {settings.DATABASE_URL}")

    from app.database import engine
    with engine.connect() as conn:
        print("    SQLAlchemy连接: OK")

except Exception as e:
    print(f"  FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("所有检查通过！")
print("=" * 60)
print("\n提示: 如果遇到注册/保存错误，运行迁移脚本:")
print("  python migrate_all_tables.py")
print("\n运行启动命令:")
print("  双击: 启动系统.bat")
print("  或手动: cd backend && python main.py")
print("\n访问地址:")
print("  前端: http://localhost:5173")
print("  API文档: http://localhost:8000/docs")
