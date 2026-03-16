"""初始化收藏表"""
from app.database import engine
from app.models import Base
from sqlalchemy import text

def init_favorites_table():
    """初始化收藏表"""
    try:
        # 创建所有表（包括 favorites）
        Base.metadata.create_all(bind=engine)

        # 检查表是否存在
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES LIKE 'favorites'"))
            if result.fetchone():
                print("✓ favorites 表已存在")
            else:
                print("✗ favorites 表不存在，尝试创建...")

        print("✓ 数据库表初始化完成")
        return True
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        return False

if __name__ == "__main__":
    init_favorites_table()
