# -*- coding: utf-8 -*-
import pymysql
from passlib.context import CryptContext

# 使用与后端相同的加密方式
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system'
)

cursor = conn.cursor()

# 重置所有用户密码为 123456
new_password = "123456"
new_hash = pwd_context.hash(new_password)

print("=" * 60)
print("重置所有用户密码")
print("=" * 60)
print(f"新密码: {new_password}")
print(f"新哈希: {new_hash}")
print()

cursor.execute("SELECT id, username FROM users")
users = cursor.fetchall()

for u in users:
    user_id, username = u
    cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user_id))
    print(f"已重置用户: {username} (ID: {user_id})")

conn.commit()
print()
print("所有密码已重置!")

cursor.close()
conn.close()
