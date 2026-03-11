"""
测试注册接口
"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("测试用户注册")
print("=" * 60)

try:
    from app.database import SessionLocal
    from app.models import User
    from app.schemas import UserCreate
    from app.utils import get_password_hash

    db = SessionLocal()

    # 测试1: 创建用户对象
    print("\n[1/3] 测试创建User对象...")
    test_user = UserCreate(
        username="testuser",
        password="123456",
        real_name="测试用户",
        student_id="S2024001",
        email="test@example.com",
        role="student",
        phone="13800138000",
        department="计算机学院",
        major="计算机科学",
        class_name="计科1班"
    )
    print("  OK - UserCreate对象创建成功")
    print(f"  用户名: {test_user.username}")
    print(f"  包含字段: {test_user.model_dump().keys()}")

    # 测试2: 创建数据库用户对象
    print("\n[2/3] 测试创建User数据库对象...")
    password_hash = get_password_hash(test_user.password)
    print(f"  密码哈希生成成功: {password_hash[:20]}...")

    db_user = User(
        username=test_user.username,
        password_hash=password_hash,
        real_name=test_user.real_name,
        student_id=test_user.student_id,
        email=test_user.email,
        role=test_user.role
    )
    print("  OK - User对象创建成功")

    # 测试3: 保存到数据库
    print("\n[3/3] 测试保存到数据库...")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"  OK - 用户保存成功，ID: {db_user.id}")

    print("\n" + "=" * 60)
    print("所有测试通过！")
    print("=" * 60)

except Exception as e:
    print(f"\n[错误] {e}")
    import traceback
    traceback.print_exc()

finally:
    if 'db' in locals():
        db.close()
