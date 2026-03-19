"""添加capacity字段到courses表"""
from app.database import engine
from sqlalchemy import text

conn = engine.connect()
try:
    conn.execute(text('ALTER TABLE courses ADD COLUMN capacity INT DEFAULT 100 COMMENT "课程容量"'))
    conn.commit()
    print("capacity字段添加成功！")
except Exception as e:
    print(f"添加失败: {e}")
    conn.rollback()
finally:
    conn.close()
