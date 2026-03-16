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

print("移除student_id的唯一约束...")

# 移除唯一约束（MySQL通过删除索引来实现）
try:
    cursor.execute("ALTER TABLE users DROP INDEX student_id")
    print("已移除student_id的唯一约束")
except Exception as e:
    print(f"可能没有约束或已移除: {e}")

conn.commit()
cursor.close()
conn.close()

print("完成!")
