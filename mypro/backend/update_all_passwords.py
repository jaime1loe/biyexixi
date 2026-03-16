"""
更新所有用户的密码哈希算法
"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import User
from app.utils import get_password_hash

def update_all_passwords():
    """更新所有用户的密码哈希"""
    print("=" * 60)
    print("更新所有用户的密码哈希算法")
    print("=" * 60)

    db = SessionLocal()

    try:
        users = db.query(User).all()
        print(f"\n找到 {len(users)} 个用户")

        # 为测试用户设置默认密码
        default_passwords = {
            'admin': 'admin123',
            'teacher': 'teacher123',
            'student1': 'student123',
            'student2': 'student123',
            'jaime': '123456',
            'younger': '123456',
            'testuser': '123456',
            '111': '123456',
            'lijm': '123456',
            'admin2': '123456'
        }

        updated_count = 0
        for user in users:
            # 使用用户名对应的密码，如果没有则使用默认密码
            password = default_passwords.get(user.username, '123456')
            user.password_hash = get_password_hash(password)
            updated_count += 1
            print(f"  - {user.username}: {password}")

        db.commit()
        print(f"\n[成功] 已更新 {updated_count} 个用户的密码")

    except Exception as e:
        print(f"\n[失败] 操作失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    print("\n" + "=" * 60)
    print("操作完成！")
    print("=" * 60)

if __name__ == '__main__':
    update_all_passwords()
