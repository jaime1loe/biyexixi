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
print("添加缺失的列到users表")
print("=" * 60)

# 检查并添加bio列
try:
    cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT AFTER class_name")
    print("[OK] 添加 bio 列成功")
except Exception as e:
    print(f"[INFO] bio列: {e}")

# 检查并添加major列
try:
    cursor.execute("ALTER TABLE users ADD COLUMN major VARCHAR(50) AFTER department")
    print("[OK] 添加 major 列成功")
except Exception as e:
    print(f"[INFO] major列: {e}")

# 检查并添加department列
try:
    cursor.execute("ALTER TABLE users ADD COLUMN department VARCHAR(50) AFTER avatar")
    print("[OK] 添加 department 列成功")
except Exception as e:
    print(f"[INFO] department列: {e}")

# 检查并添加class_name列
try:
    cursor.execute("ALTER TABLE users ADD COLUMN class_name VARCHAR(50) AFTER major")
    print("[OK] 添加 class_name 列成功")
except Exception as e:
    print(f"[INFO] class_name列: {e}")

conn.commit()

# 验证
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()
print("\n当前users表结构:")
for col in columns:
    print(f"  {col[0]} ({col[1]})")

cursor.close()
conn.close()

print("\n完成!")
