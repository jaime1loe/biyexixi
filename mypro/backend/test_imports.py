import sys
from pathlib import Path

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    print("=" * 60)
    print("测试后端导入...")
    print("=" * 60)
    
    print("\n1. 测试导入配置...")
    from backend.app.config import settings
    print(f"   [OK] 配置导入成功")
    print(f"   数据库连接: {settings.DATABASE_URL}")
    
    print("\n2. 测试导入数据库模块...")
    from backend.app.database import engine, Base
    print("   [OK] 数据库模块导入成功")
    
    print("\n3. 测试数据库连接...")
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("   [OK] 数据库连接成功")
    
    print("\n4. 测试导入路由模块...")
    from backend.app.routers import auth, questions, knowledge, feedback, statistics, users, favorites, notifications, campus
    print("   [OK] 所有路由模块导入成功")
    
    print("\n5. 测试导入异常处理...")
    from backend.app.exceptions import (
        sqlalchemy_exception_handler,
        http_exception_handler,
        validation_exception_handler
    )
    print("   [OK] 异常处理模块导入成功")
    
    print("\n6. 测试导入FastAPI...")
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.exceptions import RequestValidationError
    from sqlalchemy.exc import SQLAlchemyError
    print("   [OK] FastAPI导入成功")
    
    print("\n" + "=" * 60)
    print("后端模块导入测试全部通过！")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
