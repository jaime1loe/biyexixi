"""查看数据库中的用户"""
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

users = db.query(User).limit(10).all()
print("用户列表:")
for user in users:
    print(f"  用户名: {user.username}, 姓名: {user.real_name}, 角色: {user.role}, ID: {user.id}")

db.close()
