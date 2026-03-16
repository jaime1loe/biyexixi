# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system'
)

cursor = conn.cursor()

print("=" * 60)
print("检查并修复questions表")
print("=" * 60)

# 检查questions表结构
cursor.execute("DESCRIBE questions")
columns = {col[0] for col in cursor.fetchall()}

# 添加缺失的列
if 'ask_count' not in columns:
    try:
        cursor.execute("ALTER TABLE questions ADD COLUMN ask_count INT DEFAULT 1 AFTER views")
        print("[OK] 添加 ask_count 列")
    except Exception as e:
        print(f"[ERROR] {e}")

if 'is_public' not in columns:
    try:
        cursor.execute("ALTER TABLE questions ADD COLUMN is_public INT DEFAULT 1 AFTER ask_count")
        print("[OK] 添加 is_public 列")
    except Exception as e:
        print(f"[ERROR] {e}")

conn.commit()

# 验证
cursor.execute("DESCRIBE questions")
print("\nquestions表结构:")
for col in cursor.fetchall():
    print(f"  {col[0]} ({col[1]})")

cursor.close()
conn.close()

print("\n完成!")
