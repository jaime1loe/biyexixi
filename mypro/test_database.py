#!/usr/bin/env python3
"""
测试数据库连接和创建表的脚本
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.database import engine
    from app.models import Base
    from sqlalchemy import text
    
    print("正在连接数据库...")
    
    # 测试连接
    with engine.connect() as conn:
        print("数据库连接成功")
        
        # 检查数据库是否存在
        result = conn.execute(text("SELECT DATABASE()"))
        current_db = result.fetchone()[0]
        print(f"当前数据库: {current_db}")
        
        # 检查通知表是否存在
        result = conn.execute(text("SHOW TABLES LIKE 'notifications'"))
        if result.fetchone():
            print("✓ 通知表已存在")
        else:
            print("通知表不存在，正在创建...")
            # 创建所有表
            Base.metadata.create_all(bind=engine)
            print("数据库表创建完成")
            
        # 检查知识库表
        result = conn.execute(text("SHOW TABLES LIKE 'knowledge'"))
        if result.fetchone():
            print("知识库表已存在")
            # 检查知识库数据
            result = conn.execute(text("SELECT COUNT(*) FROM knowledge"))
            count = result.fetchone()[0]
            print(f"知识库中有 {count} 条数据")
        else:
            print("✗ 知识库表不存在")
            
        # 检查用户表
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        if result.fetchone():
            print("✓ 用户表已存在")
        else:
            print("用户表不存在")
            
    print("\n数据库检查完成！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()