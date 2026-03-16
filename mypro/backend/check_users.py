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
cursor.execute("SELECT id, username, role, email FROM users")
users = cursor.fetchall()

print("=" * 50)
print("数据库中的用户:")
print("=" * 50)
if users:
    for u in users:
        print(f"ID: {u[0]}, 用户名: {u[1]}, 角色: {u[2]}, 邮箱: {u[3]}")
else:
    print("没有用户数据!")

cursor.close()
conn.close()
