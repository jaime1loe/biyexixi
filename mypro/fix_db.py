# 完整修复数据库questions表
import pymysql
import sys

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='qa_system'
)
cursor = conn.cursor()

print("=== 检查并修复 questions 表 ===\n")

try:
    # 获取当前表结构
    cursor.execute("DESCRIBE questions")
    columns = {col[0]: col[1] for col in cursor.fetchall()}
    print("当前表字段:")
    for name, typ in columns.items():
        print(f"  - {name}: {typ}")
    
    # 检查并添加缺失字段
    if 'views' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN views INT DEFAULT 0 COMMENT '浏览次数'")
        print("\n✓ 添加 views 字段")
    
    if 'is_public' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN is_public INT DEFAULT 1 COMMENT '是否公开'")
        print("✓ 添加 is_public 字段")
    
    if 'updated_at' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'")
        print("✓ 添加 updated_at 字段")
    
    # 删除ask_count字段（如果存在）
    if 'ask_count' in columns:
        cursor.execute("ALTER TABLE questions DROP COLUMN ask_count")
        print("✓ 删除 ask_count 字段")
    
    conn.commit()
    print("\n=== 数据库修复完成 ===")
    
    # 验证
    cursor.execute("DESCRIBE questions")
    columns = [col[0] for col in cursor.fetchall()]
    print("\n修复后字段:", columns)
    
except Exception as e:
    print(f"错误: {e}")
    conn.rollback()
finally:
    conn.close()
