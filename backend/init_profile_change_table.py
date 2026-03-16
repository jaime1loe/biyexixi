"""
初始化个人信息修改申请表
"""
from app.database import engine, Base

# 导入模型
from app.models import ProfileChangeRequest

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)
    print("个人信息修改申请表创建成功")

if __name__ == "__main__":
    create_tables()
