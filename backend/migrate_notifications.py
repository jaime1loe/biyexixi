"""
通知表数据库迁移脚本
添加定时发布相关字段
"""

from sqlalchemy import text
from app.database import engine, SessionLocal


def migrate_notifications():
    """迁移通知表，添加定时发布字段"""
    db = SessionLocal()
    try:
        print("开始迁移通知表...")

        # 检查列是否已存在
        with engine.connect() as conn:
            result = conn.execute(text(
                "PRAGMA table_info(notifications)"
            ))
            existing_columns = [row[1] for row in result.fetchall()]

            if 'schedule_time' not in existing_columns:
                conn.execute(text(
                    "ALTER TABLE notifications ADD COLUMN schedule_time DATETIME"
                ))
                conn.commit()
                print("✓ 添加 schedule_time 字段")
            else:
                print("○ schedule_time 字段已存在")

            if 'status' not in existing_columns:
                conn.execute(text(
                    "ALTER TABLE notifications ADD COLUMN status VARCHAR(20) DEFAULT 'published'"
                ))
                conn.commit()
                print("✓ 添加 status 字段")

                # 更新现有记录的status
                conn.execute(text(
                    "UPDATE notifications SET status = 'published' WHERE status IS NULL"
                ))
                conn.commit()
                print("✓ 更新现有记录的status")
            else:
                print("○ status 字段已存在")

            if 'published_at' not in existing_columns:
                conn.execute(text(
                    "ALTER TABLE notifications ADD COLUMN published_at DATETIME"
                ))
                conn.commit()
                print("✓ 添加 published_at 字段")

                # 更新现有记录的published_at（使用created_at作为发布时间）
                conn.execute(text(
                    "UPDATE notifications SET published_at = created_at WHERE published_at IS NULL"
                ))
                conn.commit()
                print("✓ 更新现有记录的published_at")
            else:
                print("○ published_at 字段已存在")

        print("✅ 通知表迁移完成！")

        # 显示迁移结果
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM notifications"))
            total = result.fetchone()[0]
            print(f"\n当前通知总数: {total}")

            result = conn.execute(text(
                "SELECT status, COUNT(*) as count FROM notifications GROUP BY status"
            ))
            print("\n按状态统计:")
            for row in result.fetchall():
                print(f"  - {row[0] or 'NULL'}: {row[1]} 条")

    except Exception as e:
        print(f"❌ 迁移失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate_notifications()
