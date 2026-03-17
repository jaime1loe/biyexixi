#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解码JWT token"""
from app.utils import decode_access_token

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzczNzE2NTQ2fQ.MCyWaWJPlW9NbiVWo6JuHUnveDxKlMA3l_Xth6dlpoQ"

try:
    payload = decode_access_token(token)
    print("Token解码成功:")
    print(f"  用户ID (sub): {payload.get('sub')}")
    print(f"  过期时间 (exp): {payload.get('exp')}")
    print(f"  完整payload: {payload}")

    # 从数据库查询用户信息
    from app.database import SessionLocal
    from app.models import User

    db = SessionLocal()
    user = db.query(User).filter(User.id == int(payload.get('sub'))).first()
    if user:
        print(f"\n用户信息:")
        print(f"  ID: {user.id}")
        print(f"  用户名: {user.username}")
        print(f"  角色: {user.role}")
        print(f"  邮箱: {user.email}")
    else:
        print("\n用户不存在!")
    db.close()

except Exception as e:
    print(f"Token解码失败: {e}")
    import traceback
    traceback.print_exc()
