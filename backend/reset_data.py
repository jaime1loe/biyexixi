"""
重置数据库脚本
运行此脚本将清空所有数据并重新初始化
"""

from app.database import engine, Base
from sqlalchemy import text


def reset_database():
    """重置数据库"""
    print("正在重置数据库...")
    
    try:
        with engine.connect() as conn:
            # 删除所有表
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.commit()
            
            # 删除现有表
            Base.metadata.drop_all(bind=engine)
            
            # 重新创建表
            Base.metadata.create_all(bind=engine)
            
            print("✅ 数据库重置完成！")
            print("\n请运行 'python init_data.py' 来初始化测试数据。")
            
    except Exception as e:
        print(f"❌ 重置失败: {str(e)}")


if __name__ == "__main__":
    response = input("⚠️  警告：此操作将删除所有数据！确认继续吗？(yes/no): ")
    if response.lower() == "yes":
        reset_database()
    else:
        print("操作已取消")
