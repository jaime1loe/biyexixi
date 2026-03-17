#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试通知表"""
from app.database import engine, SessionLocal
from app.models import Notification
from sqlalchemy import text, desc

# 测试数据库连接
db = SessionLocal()
try:
    # 检查表是否存在
    result = db.execute(text("SHOW TABLES LIKE 'notifications'"))
    table_exists = result.fetchone()

    if table_exists:
        print("Table 'notifications' exists")

        # 检查表中的数据
        notifications = db.query(Notification).all()
        print(f"Total notifications: {len(notifications)}")

        for n in notifications[:3]:  # 只显示前3条
            print(f"  - ID: {n.id}, Title: {n.title}, Status: {n.status}")

        # 测试查询
        query = db.query(Notification).filter(Notification.status == "published")
        notifications = query.order_by(desc(Notification.is_important), desc(Notification.created_at)).limit(20).all()
        print(f"Query test passed: {len(notifications)} published notifications")
    else:
        print("Table 'notifications' does not exist")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

