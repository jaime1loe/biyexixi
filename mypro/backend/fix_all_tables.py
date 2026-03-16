"""修复所有缺失的数据库字段"""
from app.database import engine
from sqlalchemy import text

conn = engine.connect()

try:
    print("修复数据库表字段...")

    # 修复 questions 表
    print("\n修复 questions 表...")
    try:
        conn.execute(text("ALTER TABLE questions ADD COLUMN updated_at DATETIME COMMENT '更新时间'"))
        print("- 添加 updated_at 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- updated_at 列错误: {e}")
        else:
            print("- updated_at 列已存在")

    # 修复 knowledge 表
    print("\n修复 knowledge 表...")
    try:
        conn.execute(text("ALTER TABLE knowledge ADD COLUMN file_name VARCHAR(255) COMMENT '文件名'"))
        print("- 添加 file_name 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- file_name 列错误: {e}")
        else:
            print("- file_name 列已存在")

    try:
        conn.execute(text("ALTER TABLE knowledge ADD COLUMN file_path VARCHAR(255) COMMENT '文件路径'"))
        print("- 添加 file_path 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- file_path 列错误: {e}")
        else:
            print("- file_path 列已存在")

    try:
        conn.execute(text("ALTER TABLE knowledge ADD COLUMN file_type VARCHAR(50) COMMENT '文件类型'"))
        print("- 添加 file_type 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- file_type 列错误: {e}")
        else:
            print("- file_type 列已存在")

    try:
        conn.execute(text("ALTER TABLE knowledge ADD COLUMN file_size INT COMMENT '文件大小(字节)'"))
        print("- 添加 file_size 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- file_size 列错误: {e}")
        else:
            print("- file_size 列已存在")

    try:
        conn.execute(text("ALTER TABLE knowledge ADD COLUMN embedding TEXT COMMENT '向量数据(JSON)'"))
        print("- 添加 embedding 列")
    except Exception as e:
        if "Duplicate column" not in str(e):
            print(f"- embedding 列错误: {e}")
        else:
            print("- embedding 列已存在")

    conn.commit()
    print("\n数据库表字段修复完成!")

except Exception as e:
    print(f"修复失败: {e}")
    conn.rollback()
finally:
    conn.close()
