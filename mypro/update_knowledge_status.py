"""
将所有knowledge记录的status更新为completed
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import SessionLocal
from sqlalchemy import text

def update_all_status():
    db = SessionLocal()
    try:
        result = db.execute(text("UPDATE knowledge SET status = 'completed'"))
        db.commit()
        print(f"[OK] 已将所有 {result.rowcount} 条知识库记录的status更新为'completed'")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] 更新失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_all_status()
