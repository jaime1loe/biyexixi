#!/usr/bin/env python
"""
数据库初始化脚本
创建数据库和表结构
"""
import pymysql
from sqlalchemy import create_engine, text
from app.config import settings
from app.database import Base, engine
from app.models import User, Question, Feedback, Knowledge, Statistics


def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = connection.cursor()

        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ 数据库 {settings.DB_NAME} 创建成功")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"✗ 数据库创建失败: {e}")
        raise


def create_tables():
    """创建表结构"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据表创建成功")
    except Exception as e:
        print(f"✗ 数据表创建失败: {e}")
        raise


def verify_tables():
    """验证表是否创建成功"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"\n已创建的表: {', '.join(tables)}")
            
            expected_tables = ['users', 'questions', 'feedbacks', 'knowledge', 'statistics']
            for table in expected_tables:
                if table in tables:
                    print(f"  ✓ {table}")
                else:
                    print(f"  ✗ {table} (未找到)")
    except Exception as e:
        print(f"✗ 验证失败: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("开始初始化数据库...")
    print("=" * 50)
    
    try:
        create_database()
        create_tables()
        verify_tables()
        print("\n" + "=" * 50)
        print("数据库初始化完成！")
        print("=" * 50)
    except Exception as e:
        print(f"\n数据库初始化失败: {e}")
        exit(1)
