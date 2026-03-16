"""初始化所有数据库表"""
from app.database import engine, Base
from app.models import User, Question, Feedback, Knowledge, Statistics, Favorite, Notification

print("开始创建数据库表...")

# 创建所有表
Base.metadata.create_all(bind=engine)

print("数据库表创建完成!")

# 验证表是否创建成功
from sqlalchemy import text
conn = engine.connect()

tables = ['users', 'questions', 'feedbacks', 'knowledge', 'statistics', 'favorites', 'notifications']
for table in tables:
    try:
        result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
        count = result.fetchone()[0]
        print(f"- {table}: {count} 条记录")
    except Exception as e:
        print(f"- {table}: 错误 - {e}")

conn.close()
