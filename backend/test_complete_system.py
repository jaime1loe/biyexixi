#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整系统测试脚本
"""
import sys
import os
import io

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("完整系统测试")
print("=" * 60)

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 测试1: 导入所有模块
print("\n[1/5] 测试模块导入...")
try:
    from app.config import settings
    print("  ✓ 配置模块导入成功")
    print(f"    数据库URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"  ✗ 配置模块导入失败: {e}")
    sys.exit(1)

try:
    from app.database import engine, Base
    print("  ✓ 数据库模块导入成功")
except Exception as e:
    print(f"  ✗ 数据库模块导入失败: {e}")
    sys.exit(1)

try:
    from app.routers import auth, questions, knowledge, feedback, statistics, users, favorites, notifications, campus
    print("  ✓ 路由模块导入成功")
except Exception as e:
    print(f"  ✗ 路由模块导入失败: {e}")
    sys.exit(1)

# 测试2: 数据库连接
print("\n[2/5] 测试数据库连接...")
try:
    with engine.connect() as conn:
        print("  ✓ 数据库连接成功")
        
        # 测试简单查询
        from sqlalchemy import text
        result = conn.execute(text("SELECT VERSION()"))
        version = result.fetchone()[0]
        print(f"    MySQL版本: {version}")
        
        # 检查表是否存在
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        if tables:
            print(f"    ✓ 发现 {len(tables)} 张表")
        else:
            print("    ⚠ 数据库中无表，系统将自动创建")
        
except Exception as e:
    print(f"  ✗ 数据库连接失败: {e}")
    print("\n  解决方案:")
    print("  1. 确保MySQL服务已启动: net start mysql")
    print("  2. 检查配置文件: backend/app/config.py")
    print("  3. 检查数据库名: qa_system")
    print("  4. 检查用户名/密码")
    sys.exit(1)

# 测试3: 检查主要模型
print("\n[3/5] 测试数据模型...")
try:
    from app.models import User, Question, Feedback, Knowledge, Statistics
    
    # 尝试创建表（如果不存在）
    print("  检查数据表结构...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ 数据表结构正常")
    
except Exception as e:
    print(f"  ✗ 数据模型检查失败: {e}")
    sys.exit(1)

# 测试4: 检查路由导入
print("\n[4/5] 测试路由处理器...")
try:
    # 测试所有路由导入
    print("  导入所有路由...")
    
    from fastapi import FastAPI
    app = FastAPI()
    
    # 注册路由（不实际运行）
    app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
    app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
    app.include_router(questions.router, prefix="/api/questions", tags=["问答"])
    app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
    app.include_router(feedback.router, prefix="/api/feedback", tags=["反馈"])
    app.include_router(statistics.router, prefix="/api/statistics", tags=["统计"])
    app.include_router(favorites.router, prefix="/api/favorites", tags=["收藏"])
    app.include_router(notifications.router, prefix="/api/notifications", tags=["通知"])
    app.include_router(campus.router, prefix="/api/campus", tags=["校园服务"])
    
    print("  ✓ 所有路由导入成功")
    
except Exception as e:
    print(f"  ✗ 路由导入失败: {e}")
    sys.exit(1)

# 测试5: 尝试启动应用
print("\n[5/5] 测试应用启动...")
try:
    # 检查main.py语法
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    import ast
    ast.parse(code)
    print("  ✓ main.py语法检查通过")
    
    # 测试导入main.py
    import main as backend_main
    print("  ✓ FastAPI应用导入成功")
    print(f"    应用名称: {backend_main.app.title}")
    print(f"    版本号: {backend_main.app.version}")
    
    print("\n" + "=" * 60)
    print("系统测试全部通过！")
    print("=" * 60)
    print("\n启动命令:")
    print("  cd d:\\毕业设计\\backend")
    print("  python main.py")
    
except SyntaxError as e:
    print(f"  ✗ 语法错误: {e}")
    print(f"    错误位置: {e.filename}:{e.lineno}")
    print(f"    错误内容: {e.text}")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ 启动测试失败: {e}")
    sys.exit(1)