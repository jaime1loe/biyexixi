#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
后端程序测试和启动脚本
"""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("基于大模型智能体的高校知识库在线答疑系统")
print("后端服务启动测试")
print("=" * 60)

# 添加backend到路径
sys.path.insert(0, 'd:/毕业设计')

try:
    print("\n1. 测试模块导入...")
    from backend.app.config import settings
    print(f"   [OK] 配置加载成功")
    print(f"   数据库: {settings.DB_NAME}")
    print(f"   端口: {settings.PORT}")

    print("\n2. 测试数据库连接...")
    from backend.app.database import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"   [OK] 数据库连接成功")

    print("\n3. 测试FastAPI应用...")
    from main import app
    print(f"   [OK] FastAPI应用加载成功")
    print(f"   应用名称: {app.title}")
    print(f"   API路由数: {len(app.routes)}")

    print("\n" + "=" * 60)
    print("[OK] 所有测试通过！")
    print("=" * 60)
    print("\n启动命令:")
    print("  cd backend")
    print("  python main.py")
    print("\n访问地址:")
    print("  API文档: http://localhost:8000/docs")
    print("  根路径: http://localhost:8000")

except Exception as e:
    print(f"\n[FAIL] 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
