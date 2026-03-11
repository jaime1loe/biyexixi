#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重置数据库数据（自动确认）
"""
import sys
import io

# 设置stdout编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy import text
from app.database import engine


def reset_database():
    """重置数据库表数据"""
    tables = ['feedbacks', 'questions', 'knowledge', 'users', 'statistics']

    print("[WARN] 警告：即将删除所有数据！")

    try:
        with engine.connect() as conn:
            # 禁用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            for table in tables:
                conn.execute(text(f"TRUNCATE TABLE {table}"))
                print(f"[OK] 已清空表: {table}")

            # 启用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

            conn.commit()

        print("\n[OK] 数据库重置完成")
    except Exception as e:
        print(f"[FAIL] 重置失败: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("重置数据库")
    print("=" * 50)
    reset_database()
