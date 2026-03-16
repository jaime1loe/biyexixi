# -*- coding: utf-8 -*-
import pymysql
import sys
sys.path.insert(0, '.')

print("=" * 50)
print("数据库连接诊断")
print("=" * 50)

# 测试1: 读取配置
print("\n[1] 读取配置...")
try:
    from app.config import settings
    print(f"   DB_HOST: {settings.DB_HOST}")
    print(f"   DB_PORT: {settings.DB_PORT}")
    print(f"   DB_NAME: {settings.DB_NAME}")
    print(f"   DB_USER: {settings.DB_USER}")
    print(f"   DB_PASSWORD: {'*' * len(settings.DB_PASSWORD)}")
except Exception as e:
    print(f"   [错误] 读取配置失败: {e}")
    sys.exit(1)

# 测试2: 连接MySQL服务器
print("\n[2] 连接MySQL服务器...")
try:
    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        connect_timeout=5
    )
    print("   [成功] 连接到MySQL服务器")
    conn.close()
except Exception as e:
    print(f"   [错误] 连接失败: {e}")
    print("   请检查: MySQL服务是否启动? 密码是否正确?")
    sys.exit(1)

# 测试3: 连接数据库
print("\n[3] 连接数据库 qa_system...")
try:
    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        connect_timeout=5
    )
    print(f"   [成功] 连接到数据库 {settings.DB_NAME}")
except Exception as e:
    print(f"   [错误] 数据库连接失败: {e}")
    print(f"   数据库 '{settings.DB_NAME}' 是否已创建?")
    sys.exit(1)

# 测试4: 检查表
print("\n[4] 检查数据库表...")
cursor = conn.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(f"   数据库中共有 {len(tables)} 张表:")
for t in tables:
    print(f"   - {t[0]}")

cursor.close()
conn.close()

print("\n" + "=" * 50)
print("数据库连接正常!")
print("=" * 50)
