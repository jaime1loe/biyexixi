import sys
import io

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.utils import get_password_hash

print("=" * 60)
print("测试用户注册")
print("=" * 60)

try:
    # 创建数据库会话
    db = SessionLocal()

    # 模拟注册数据
    test_user = UserCreate(
        username="testuser999",
        password="123456",
        real_name="测试用户",
        student_id="202403111999",
        email="test999@example.com",
        role="student"
    )

    print(f"\n尝试创建用户:")
    print(f"  用户名: {test_user.username}")
    print(f"  真实姓名: {test_user.real_name}")
    print(f"  学号: {test_user.student_id}")
    print(f"  邮箱: {test_user.email}")
    print(f"  角色: {test_user.role}")

    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == test_user.username).first()
    if existing_user:
        print(f"\n[错误] 用户名 {test_user.username} 已存在")
        db.close()
        sys.exit(1)

    # 检查学号是否存在
    if test_user.student_id:
        existing_student = db.query(User).filter(User.student_id == test_user.student_id).first()
        if existing_student:
            print(f"\n[错误] 学号 {test_user.student_id} 已存在")
            db.close()
            sys.exit(1)

    # 创建新用户
    password_hash = get_password_hash(test_user.password)
    db_user = User(
        username=test_user.username,
        password_hash=password_hash,
        real_name=test_user.real_name,
        student_id=test_user.student_id,
        email=test_user.email,
        role=test_user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"\n[成功] 用户创建成功!")
    print(f"  用户ID: {db_user.id}")
    print(f"  创建时间: {db_user.created_at}")

    db.close()

except Exception as e:
    print(f"\n[错误] 注册失败: {e}")
    import traceback
    traceback.print_exc()
    db.close()
    sys.exit(1)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
