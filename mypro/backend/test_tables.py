"""测试通知表和问题表"""
from app.database import engine, get_db
from app.models import Notification, Question
from sqlalchemy import text

# 测试通知表
print("测试通知表...")
conn = engine.connect()
try:
    result = conn.execute(text('SELECT COUNT(*) FROM notifications'))
    count = result.fetchone()[0]
    print(f"✓ 通知表存在，共有 {count} 条记录")
except Exception as e:
    print(f"✗ 通知表错误: {e}")
finally:
    conn.close()

# 测试问题表
print("\n测试问题表...")
conn = engine.connect()
try:
    result = conn.execute(text('SELECT COUNT(*) FROM questions'))
    count = result.fetchone()[0]
    print(f"✓ 问题表存在，共有 {count} 条记录")
except Exception as e:
    print(f"✗ 问题表错误: {e}")
finally:
    conn.close()

print("\n测试完成!")
