#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查当前用户信息"""
from app.database import engine, SessionLocal
from app.models import User
from sqlalchemy import text, desc

db = SessionLocal()
try:
    # 查询所有用户
    users = db.query(User).order_by(desc(User.id)).limit(5).all()
    print(f"Total users in database: {db.query(User).count()}")
    print("\nRecent users:")
    for user in users:
        print(f"  - ID: {user.id}, Username: {user.username}, Role: {user.role}, Email: {user.email}")

    # 查询管理员用户
    admin_users = db.query(User).filter(User.role == "admin").all()
    print(f"\nAdmin users: {len(admin_users)}")
    for user in admin_users:
        print(f"  - ID: {user.id}, Username: {user.username}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
