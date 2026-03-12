"""
初始化数据库表
"""

import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine, Base
from app.models import User, Question, Feedback, Knowledge, Statistics, Favorite, Notification

def init_tables():
    """初始化数据库表"""
    print("=" * 60)
    print("初始化数据库表")
    print("=" * 60)

    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("\n[成功] 数据库表创建成功！")

        # 列出所有表
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print("\n当前数据库中的表:")
        for table in tables:
            print(f"  - {table}")

        print("\n" + "=" * 60)
        print("初始化完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n[失败] 初始化失败: {e}")
        raise


if __name__ == '__main__':
    init_tables()
