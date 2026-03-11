import sys
from pathlib import Path

# 添加backend目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.config import settings
from app.database import engine
from sqlalchemy import text

print("✅ 配置加载成功")
print(f"数据库名: {settings.DATABASE_NAME}")
print(f"调试模式: {settings.DEBUG}")
print(f"应用名称: {settings.APP_NAME}")

# 测试数据库连接
try:
    conn = engine.connect()
    conn.execute(text("SELECT 1"))
    conn.close()
    print("✅ 数据库连接成功")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
