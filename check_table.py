import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('DESCRIBE notifications'))
    print("通知表结构:")
    for row in result:
        print(row)
    
    result = conn.execute(text('SELECT * FROM notifications LIMIT 1'))
    print("\n通知表数据示例:")
    for row in result:
        print(row)