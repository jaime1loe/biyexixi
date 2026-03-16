# -*- coding: utf-8 -*-
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()
cursor.execute("SELECT username, role, email FROM users WHERE role='admin'")
print("管理员账号:")
for u in cursor.fetchall():
    print(f"  用户名: {u[0]}, 邮箱: {u[2]}")
conn.close()
