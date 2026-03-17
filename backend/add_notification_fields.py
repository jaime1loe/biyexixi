#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为notifications表添加定时发布相关字段"""
from sqlalchemy import text
from app.database import engine

with engine.connect() as conn:
    # 检查表结构
    result = conn.execute(text("DESCRIBE notifications"))
    columns = [row[0] for row in result.fetchall()]
    print(f"Current columns: {columns}")

    # 添加 schedule_time 字段
    if 'schedule_time' not in columns:
        print("Adding schedule_time column...")
        conn.execute(text("ALTER TABLE notifications ADD COLUMN schedule_time DATETIME COMMENT '定时发布时间'"))
        print("Added schedule_time column")
    else:
        print("schedule_time column already exists")

    # 添加 status 字段
    if 'status' not in columns:
        print("Adding status column...")
        conn.execute(text("ALTER TABLE notifications ADD COLUMN status VARCHAR(20) DEFAULT 'published' COMMENT '状态: published=已发布, scheduled=待定时, draft=草稿'"))
        print("Added status column")
    else:
        print("status column already exists")

    # 添加 published_at 字段
    if 'published_at' not in columns:
        print("Adding published_at column...")
        conn.execute(text("ALTER TABLE notifications ADD COLUMN published_at DATETIME COMMENT '实际发布时间'"))
        print("Added published_at column")
    else:
        print("published_at column already exists")

    # 提交事务
    conn.commit()
    print("\nMigration completed successfully!")
