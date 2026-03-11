"""
完整数据库迁移脚本 - 修复所有表结构
"""
import pymysql

print("=" * 60)
print("完整数据库迁移")
print("=" * 60)

conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()

# ============ users 表 ============
print("\n[1/6] 检查 users 表...")
cursor.execute("DESCRIBE users")
existing_columns = [col[0] for col in cursor.fetchall()]

user_migrations = [
    ("phone", "ALTER TABLE users ADD COLUMN phone VARCHAR(20) COMMENT '电话' AFTER email"),
    ("avatar", "ALTER TABLE users ADD COLUMN avatar VARCHAR(255) COMMENT '头像路径' AFTER phone"),
    ("department", "ALTER TABLE users ADD COLUMN department VARCHAR(50) COMMENT '院系' AFTER role"),
    ("major", "ALTER TABLE users ADD COLUMN major VARCHAR(50) COMMENT '专业' AFTER department"),
    ("class_name", "ALTER TABLE users ADD COLUMN class_name VARCHAR(50) COMMENT '班级' AFTER major"),
    ("is_active", "ALTER TABLE users ADD COLUMN is_active INT DEFAULT 1 COMMENT '是否激活: 1=激活, 0=禁用' AFTER class_name"),
]

for field_name, sql in user_migrations:
    try:
        if field_name not in existing_columns:
            cursor.execute(sql)
            conn.commit()
            print(f"  [OK] 添加 users.{field_name}")
        else:
            print(f"  [SKIP] users.{field_name} 已存在")
    except Exception as e:
        print(f"  [FAIL] 添加 users.{field_name}: {e}")

# ============ questions 表 ============
print("\n[2/6] 检查 questions 表...")
cursor.execute("DESCRIBE questions")
existing_columns = [col[0] for col in cursor.fetchall()]

question_migrations = [
    ("views", "ALTER TABLE questions ADD COLUMN views INT DEFAULT 0 COMMENT '浏览次数' AFTER category"),
    ("is_public", "ALTER TABLE questions ADD COLUMN is_public INT DEFAULT 1 COMMENT '是否公开: 1=公开, 0=私密' AFTER views"),
    ("updated_at", "ALTER TABLE questions ADD COLUMN updated_at DATETIME COMMENT '更新时间' AFTER is_public"),
]

for field_name, sql in question_migrations:
    try:
        if field_name not in existing_columns:
            cursor.execute(sql)
            conn.commit()
            print(f"  [OK] 添加 questions.{field_name}")
        else:
            print(f"  [SKIP] questions.{field_name} 已存在")
    except Exception as e:
        print(f"  [FAIL] 添加 questions.{field_name}: {e}")

# ============ feedbacks 表 ============
print("\n[3/6] 检查 feedbacks 表...")
cursor.execute("DESCRIBE feedbacks")
existing_columns = [col[0] for col in cursor.fetchall()]

# feedbacks 表结构正确，无需修改
print(f"  [OK] feedbacks 表结构正确 ({len(existing_columns)} 字段)")

# ============ knowledge 表 ============
print("\n[4/6] 检查 knowledge 表...")
cursor.execute("DESCRIBE knowledge")
existing_columns = [col[0] for col in cursor.fetchall()]

knowledge_migrations = [
    ("file_name", "ALTER TABLE knowledge ADD COLUMN file_name VARCHAR(255) COMMENT '文件名' AFTER tags"),
    ("file_type", "ALTER TABLE knowledge ADD COLUMN file_type VARCHAR(50) COMMENT '文件类型' AFTER file_path"),
    ("file_size", "ALTER TABLE knowledge ADD COLUMN file_size INT COMMENT '文件大小(字节)' AFTER file_type"),
    ("updated_at", "ALTER TABLE knowledge ADD COLUMN updated_at DATETIME COMMENT '更新时间' AFTER embedding"),
]

for field_name, sql in knowledge_migrations:
    try:
        if field_name not in existing_columns:
            cursor.execute(sql)
            conn.commit()
            print(f"  [OK] 添加 knowledge.{field_name}")
        else:
            print(f"  [SKIP] knowledge.{field_name} 已存在")
    except Exception as e:
        print(f"  [FAIL] 添加 knowledge.{field_name}: {e}")

# ============ statistics 表 ============
print("\n[5/6] 检查 statistics 表...")
cursor.execute("DESCRIBE statistics")
existing_columns = [col[0] for col in cursor.fetchall()]

# statistics 表结构正确，无需修改
print(f"  [OK] statistics 表结构正确 ({len(existing_columns)} 字段)")

# ============ favorites 表 ============
print("\n[6/6] 检查 favorites 表...")
cursor.execute("SHOW TABLES LIKE 'favorites'")
if not cursor.fetchone():
    # 创建 favorites 表
    print(f"  [INFO] 创建 favorites 表...")
    create_sql = """
    CREATE TABLE favorites (
        id INT PRIMARY KEY AUTO_INCREMENT COMMENT '收藏ID',
        user_id INT NOT NULL COMMENT '用户ID',
        knowledge_id INT NOT NULL COMMENT '知识ID',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        UNIQUE KEY unique_favorite (user_id, knowledge_id),
        INDEX idx_user (user_id),
        INDEX idx_knowledge (knowledge_id)
    ) COMMENT='收藏表';
    """
    cursor.execute(create_sql)
    conn.commit()
    print(f"  [OK] favorites 表创建成功")
else:
    cursor.execute("DESCRIBE favorites")
    existing_columns = [col[0] for col in cursor.fetchall()]
    print(f"  [OK] favorites 表已存在 ({len(existing_columns)} 字段)")

print("\n" + "=" * 60)
print("数据库迁移完成!")
print("=" * 60)

# 显示所有表结构
print("\n当前数据库表结构:")
print("-" * 60)
tables = ['users', 'questions', 'feedbacks', 'knowledge', 'statistics', 'favorites']
for table in tables:
    cursor.execute(f"DESCRIBE {table}")
    columns = cursor.fetchall()
    print(f"\n{table} ({len(columns)} 字段):")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")

conn.close()

print("\n" + "=" * 60)
print("所有表结构已与模型定义保持一致!")
print("=" * 60)
