import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='qa_system'
)
cursor = conn.cursor()

try:
    # 获取表结构
    cursor.execute("DESCRIBE questions")
    columns = {col[0]: col[1] for col in cursor.fetchall()}
    print("=== Questions 表结构 ===")
    for name, typ in columns.items():
        print(f"  {name}: {typ}")

    # 检查必要字段
    required_fields = ['id', 'user_id', 'question', 'answer', 'category', 'views', 'ask_count', 'is_public', 'created_at', 'updated_at']
    print("\n=== 字段检查 ===")
    for field in required_fields:
        status = "✓" if field in columns else "✗"
        print(f"  {status} {field}")

    # 尝试查询
    print("\n=== 测试查询 ===")
    cursor.execute("SELECT * FROM questions LIMIT 1")
    row = cursor.fetchone()
    print(f"查询成功，数据: {row}")

except Exception as e:
    print(f"错误: {e}")
finally:
    conn.close()
