import pymysql
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("测试MySQL数据库连接...")
print("=" * 50)

try:
    # 测试连接到MySQL服务器
    print("\n1. 测试连接到MySQL服务器...")
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        connect_timeout=5
    )
    print("   [OK] 成功连接到MySQL服务器")
    conn.close()
    
    # 测试连接到数据库
    print("\n2. 测试连接到数据库 qa_system...")
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        database='qa_system',
        connect_timeout=5
    )
    print("   [OK] 成功连接到数据库 qa_system")
    
    # 测试查询
    print("\n3. 测试查询...")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"   [OK] 数据库中有 {len(tables)} 张表")
    if tables:
        print(f"   表列表: {', '.join([t[0] for t in tables])}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 50)
    print("数据库连接测试成功！")
    
except pymysql.Error as e:
    print(f"\n[ERROR] 数据库连接失败!")
    print(f"错误代码: {e.args[0]}")
    print(f"错误信息: {e.args[1]}")
    
    if e.args[0] == 1045:
        print("\n提示：用户名或密码错误")
    elif e.args[0] == 2003:
        print("\n提示：无法连接到MySQL服务器，请检查服务是否启动")
    elif e.args[0] == 1049:
        print("\n提示：数据库不存在，请先创建数据库")
    
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] 未知错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
