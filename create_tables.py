#!/usr/bin/env python3
"""
创建数据库表的脚本
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine
from app.models import Base

def main():
    print("正在创建数据库表...")
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建完成")
        
        # 检查表是否创建成功
        from sqlalchemy import text
        with engine.connect() as conn:
            # 检查通知表
            result = conn.execute(text("SHOW TABLES LIKE 'notifications'"))
            if result.fetchone():
                print("✓ 通知表已存在")
            else:
                print("✗ 通知表创建失败")
                
            # 检查知识库表
            result = conn.execute(text("SHOW TABLES LIKE 'knowledge'"))
            if result.fetchone():
                print("✓ 知识库表已存在")
            else:
                print("✗ 知识库表创建失败")
                
    except Exception as e:
        print(f"✗ 创建数据库表时出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())