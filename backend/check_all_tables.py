"""
检查所有表的结构是否与模型匹配
"""
import pymysql
import sys
sys.path.insert(0, '.')

conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()

print("=" * 60)
print("数据库表结构检查")
print("=" * 60)

tables = ['users', 'questions', 'feedbacks', 'knowledge', 'statistics', 'favorites']

for table in tables:
    try:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        print(f"\n{table} 表 ({len(columns)} 字段):")
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
    except Exception as e:
        print(f"\n{table} 表: [错误] {e}")

conn.close()

print("\n" + "=" * 60)
