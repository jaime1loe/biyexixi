"""测试数据库表是否存在"""
from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

print("数据库中的表:")
for table in tables:
    print(f"  - {table}")

if 'course_selections' in tables:
    print("\ncourse_selections 表已存在")
    columns = inspector.get_columns('course_selections')
    print("表结构:")
    for col in columns:
        print(f"  {col['name']}: {col['type']}")
else:
    print("\ncourse_selections 表不存在，需要创建")

# 尝试创建表
from app.models import CourseSelection, Base
print("\n尝试创建 course_selections 表...")
try:
    Base.metadata.create_all(bind=engine)
    print("创建成功！")
except Exception as e:
    print(f"创建失败: {e}")
