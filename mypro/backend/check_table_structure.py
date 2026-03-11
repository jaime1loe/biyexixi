import pymysql

conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()

print("数据库表结构检查")
print("=" * 60)

cursor.execute("DESCRIBE users")
columns = cursor.fetchall()

print("\nusers表结构:")
print("-" * 60)
for col in columns:
    field_name = col[0] or ""
    field_type = col[1] or ""
    null = col[2] or ""
    key = col[3] or ""
    default = str(col[4]) if col[4] is not None else ""
    print(f"  {field_name:20} {field_type:20} {null:5} {key:5} {default:10}")

conn.close()
