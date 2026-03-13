"""
数据库迁移脚本 - 添加缺失的字段
"""
import pymysql

print("=" * 60)
print("数据库迁移 - 添加缺失字段")
print("=" * 60)

conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()

# 检查表结构
cursor.execute("DESCRIBE users")
existing_columns = [col[0] for col in cursor.fetchall()]

print("\n当前users表字段:")
for col in existing_columns:
    print(f"  - {col}")

# 需要添加的字段
migrations = [
    ("phone", "ALTER TABLE users ADD COLUMN phone VARCHAR(20) COMMENT '电话' AFTER email"),
    ("avatar", "ALTER TABLE users ADD COLUMN avatar VARCHAR(255) COMMENT '头像路径' AFTER phone"),
    ("department", "ALTER TABLE users ADD COLUMN department VARCHAR(50) COMMENT '院系' AFTER role"),
    ("major", "ALTER TABLE users ADD COLUMN major VARCHAR(50) COMMENT '专业' AFTER department"),
    ("class_name", "ALTER TABLE users ADD COLUMN class_name VARCHAR(50) COMMENT '班级' AFTER major"),
    ("is_active", "ALTER TABLE users ADD COLUMN is_active INT DEFAULT 1 COMMENT '是否激活: 1=激活, 0=禁用' AFTER class_name"),
]

print("\n开始迁移...")
print("-" * 60)

success_count = 0
for field_name, sql in migrations:
    try:
        if field_name not in existing_columns:
            cursor.execute(sql)
            conn.commit()
            print(f"  [OK] 添加字段: {field_name}")
            success_count += 1
        else:
            print(f"  [SKIP] 字段已存在: {field_name}")
            success_count += 1
    except Exception as e:
        print(f"  [FAIL] 添加字段 {field_name} 失败: {e}")

print("-" * 60)
print(f"迁移完成! 成功: {success_count}/{len(migrations)}")

# 显示更新后的表结构
print("\n更新后的users表结构:")
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()
for col in columns:
    print(f"  - {col[0]} ({col[1]})")

conn.close()

print("\n" + "=" * 60)
print("现在可以正常注册用户了！")
print("=" * 60)
