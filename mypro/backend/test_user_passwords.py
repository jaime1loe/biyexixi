# -*- coding: utf-8 -*-
import pymysql
from passlib.hash import bcrypt

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system'
)

cursor = conn.cursor()
cursor.execute("SELECT id, username, password_hash FROM users")
users = cursor.fetchall()

print("=" * 60)
print("测试用户密码")
print("=" * 60)

test_passwords = ["123456", "12345678", "123", "password", "1234567", "liujiaxin"]

for u in users:
    user_id, username, pwd_hash = u
    print(f"\n用户: {username} (ID: {user_id})")
    print(f"密码哈希: {pwd_hash[:50]}...")
    
    # 测试常见密码
    for pwd in test_passwords:
        try:
            if bcrypt.verify(pwd, pwd_hash):
                print(f"  >>> 密码是: {pwd}")
                break
        except:
            pass
    else:
        print(f"  未找到匹配密码")

cursor.close()
conn.close()
