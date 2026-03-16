"""
重置管理员密码
"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import engine, Base, SessionLocal
from app.models import User
from app.utils import get_password_hash
from sqlalchemy import text

def reset_admin_password():
    """重置管理员密码"""
    print("=" * 60)
    print("重置管理员密码")
    print("=" * 60)

    db = SessionLocal()

    try:
        # 查找或创建管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()

        if not admin_user:
            print("\n[创建] 管理员用户不存在，正在创建...")
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                real_name="系统管理员",
                role="admin",
                is_active=1
            )
            db.add(admin_user)
            db.commit()
            print("[成功] 管理员用户创建成功！")
        else:
            print("\n[更新] 管理员用户已存在，正在重置密码...")
            admin_user.password_hash = get_password_hash("admin123")
            admin_user.is_active = 1
            db.commit()
            print("[成功] 管理员密码重置成功！")

        print("\n管理员信息:")
        print(f"  用户名: admin")
        print(f"  密码: admin123")
        print(f"  角色: {admin_user.role}")

        # 列出所有用户
        print("\n数据库中的所有用户:")
        users = db.query(User).all()
        for u in users:
            print(f"  - ID: {u.id}, 用户名: {u.username}, 角色: {u.role}, 激活: {u.is_active}")

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
    reset_admin_password()
