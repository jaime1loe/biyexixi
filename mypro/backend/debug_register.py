# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("调试注册功能")
print("=" * 60)

# 测试数据库连接
print("\n[1] 测试数据库连接...")
try:
    from app.database import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("   [OK] 数据库连接正常")
except Exception as e:
    print(f"   [ERROR] 数据库连接失败: {e}")
    sys.exit(1)

# 测试User模型
print("\n[2] 测试User模型...")
try:
    from app.models import User
    print("   [OK] User模型导入成功")
except Exception as e:
    print(f"   [ERROR] User模型导入失败: {e}")
    sys.exit(1)

# 测试Schema
print("\n[3] 测试UserCreate Schema...")
try:
    from app.schemas import UserCreate
    test_user = UserCreate(
        username="test123",
        password="123456",
        email="test@test.com",
        role="student"
    )
    print(f"   [OK] Schema创建成功: {test_user}")
except Exception as e:
    print(f"   [ERROR] Schema创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试创建用户
print("\n[4] 测试创建用户...")
try:
    from app.database import SessionLocal
    from app.models import User
    from app.utils import get_password_hash

    db = SessionLocal()
    new_user = User(
        username="debug_test",
        password_hash=get_password_hash("123456"),
        email="debug@test.com",
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"   [OK] 用户创建成功: ID={new_user.id}, username={new_user.username}")

    # 删除测试用户
    db.delete(new_user)
    db.commit()
    print("   [OK] 测试用户已清理")

    db.close()
except Exception as e:
    print(f"   [ERROR] 创建用户失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("所有测试通过!")
print("=" * 60)
