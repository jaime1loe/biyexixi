from app.database import engine
from app.models import User
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# 查找管理员用户
admin = session.query(User).filter(User.username == "admin").first()

if admin:
    print(f"管理员用户:")
    print(f"  ID: {admin.id}")
    print(f"  用户名: {admin.username}")
    print(f"  邮箱: {admin.email}")
    print(f"  角色: {admin.role}")
else:
    print("未找到管理员用户")

session.close()
