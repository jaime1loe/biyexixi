from app.database import engine
from app.models import User
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# 查找所有用户
users = session.query(User).limit(5).all()

print("系统中的用户:")
for user in users:
    print(f"  ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 角色: {user.role}")

session.close()
