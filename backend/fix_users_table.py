import sys
import io

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pymysql
from app.config import settings

print("=" * 60)
print("修复 users 表结构")
print("=" * 60)

try:
    # 连接数据库
    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    # 检查当前表结构
    print("\n1. 检查当前表结构...")
    cursor.execute("SHOW COLUMNS FROM users")
    columns = [row[0] for row in cursor.fetchall()]
    print(f"   当前字段: {', '.join(columns)}")

    # 需要添加的字段
    new_columns = {
        'phone': "VARCHAR(20) COMMENT '电话'",
        'avatar': "VARCHAR(255) COMMENT '头像路径'",
        'department': "VARCHAR(50) COMMENT '院系'",
        'major': "VARCHAR(50) COMMENT '专业'",
        'class_name': "VARCHAR(50) COMMENT '班级'",
        'is_active': "INT DEFAULT 1 COMMENT '是否激活: 1=激活, 0=禁用'",
        'updated_at': "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'"
    }

    print("\n2. 添加缺失的字段...")
    for column_name, column_def in new_columns.items():
        if column_name not in columns:
            print(f"   添加字段 {column_name}...")
            sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_def}"
            cursor.execute(sql)
            print(f"   ✓ {column_name} 添加成功")
        else:
            print(f"   ⊘ {column_name} 已存在")

    # 检查 password_hash 字段
    print("\n3. 检查 password_hash 字段...")
    cursor.execute("SHOW COLUMNS FROM users LIKE 'password_hash'")
    result = cursor.fetchone()
    if not result:
        print("   添加 password_hash 字段...")
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255) COMMENT '密码哈希'")
        print("   ✓ password_hash 添加成功")
    else:
        print("   ✓ password_hash 已存在")

    conn.commit()

    print("\n4. 验证表结构...")
    cursor.execute("SHOW COLUMNS FROM users")
    columns = cursor.fetchall()
    print("\n更新后的表结构:")
    for col in columns:
        print(f"  {col[0]:20s} {col[1]:30s} {col[3] if len(col) > 3 else ''}")

    cursor.close()
    conn.close()

    print("\n" + "=" * 60)
    print("表结构修复完成！")
    print("=" * 60)

except Exception as e:
    print(f"\n[错误] 修复失败: {e}")
    import traceback
    traceback.print_exc()
    if 'conn' in locals():
        conn.rollback()
        conn.close()
    sys.exit(1)
