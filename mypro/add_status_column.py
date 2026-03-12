"""
添加status字段到knowledge表
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import engine, SessionLocal
from sqlalchemy import text
import sqlalchemy

def add_status_column():
    """添加status字段到knowledge表"""
    db = SessionLocal()
    try:
        # 检查status字段是否已存在
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'knowledge'
            AND COLUMN_NAME = 'status'
        """))
        exists = result.fetchone()[0] > 0

        if exists:
            print("status字段已存在，无需添加")
            return

        # 添加status字段
        db.execute(text("""
            ALTER TABLE knowledge
            ADD COLUMN status VARCHAR(20) DEFAULT 'pending'
            COMMENT '状态: pending=待处理, processing=处理中, completed=已完成, failed=失败'
        """))
        db.commit()
        print("[OK] 成功添加status字段到knowledge表")

        # 更新现有记录的status为completed
        db.execute(text("""
            UPDATE knowledge SET status = 'completed' WHERE status IS NULL
        """))
        db.commit()
        print("[OK] 已将现有记录的status更新为'completed'")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] 添加字段失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_status_column()
