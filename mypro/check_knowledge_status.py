"""
检查并更新knowledge表中的status字段
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import engine, SessionLocal
from sqlalchemy import text

def check_and_update_status():
    """检查并更新status字段"""
    db = SessionLocal()
    try:
        # 查看knowledge表的结构
        result = db.execute(text("DESCRIBE knowledge"))
        columns = result.fetchall()
        print("Knowledge表结构:")
        for col in columns:
            print(f"  {col[0]}: {col[1]}")

        print("\n")

        # 查看前5条记录
        result = db.execute(text("SELECT id, title, status FROM knowledge LIMIT 5"))
        records = result.fetchall()
        print("前5条记录:")
        for record in records:
            print(f"  ID: {record[0]}, Title: {record[1]}, Status: {record[2]}")

        print("\n")

        # 更新所有NULL或空字符串的status为completed
        result = db.execute(text("""
            UPDATE knowledge
            SET status = 'completed'
            WHERE status IS NULL OR status = ''
        """))
        db.commit()
        print(f"[OK] 已更新 {result.rowcount} 条记录的status为'completed'")

        # 验证更新结果
        result = db.execute(text("""
            SELECT status, COUNT(*) as count
            FROM knowledge
            GROUP BY status
        """))
        print("\n各状态的文档数量:")
        for row in result.fetchall():
            print(f"  {row[0]}: {row[1]}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] 操作失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_and_update_status()
