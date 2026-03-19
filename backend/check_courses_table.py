"""检查courses表结构"""
from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
columns = inspector.get_columns('courses')

print("courses 表结构:")
for col in columns:
    print(f"  {col['name']}: {col['type']}")
