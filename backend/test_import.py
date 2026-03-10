"""测试后端导入和数据库连接"""
import sys
import traceback
import io

# 设置stdout编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("测试后端程序")
print("=" * 60)

try:
    print("\n1. 导入配置...")
    from app.config import settings
    print(f"   [OK] 配置加载成功")
    print(f"   数据库URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"   [FAIL] 配置加载失败: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n2. 测试数据库连接...")
    from app.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(f"   [OK] 数据库连接成功")
except Exception as e:
    print(f"   [FAIL] 数据库连接失败: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n3. 创建数据库表...")
    from app.database import Base
    from app.models import User, Question, Feedback, Knowledge, Statistics

    Base.metadata.create_all(bind=engine)
    print(f"   [OK] 数据库表创建成功")
except Exception as e:
    print(f"   [FAIL] 数据库表创建失败: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n4. 导入FastAPI应用...")
    from main import app
    print(f"   [OK] FastAPI应用加载成功")
    print(f"   应用名称: {app.title}")
    print(f"   路由数量: {len(app.routes)}")
except Exception as e:
    print(f"   [FAIL] FastAPI应用加载失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] 所有测试通过！后端程序可以正常运行")
print("=" * 60)
print("\n启动命令: python main.py")
print("API文档: http://localhost:8000/docs")
