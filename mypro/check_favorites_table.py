#!/usr/bin/env python3
"""
检查收藏表结构
"""

import mysql.connector

def check_favorites_table():
    """检查收藏表结构"""
    try:
        # 连接数据库
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='qa_system'
        )
        cursor = conn.cursor()
        
        print("=== 检查收藏表结构 ===")
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'favorites'")
        if not cursor.fetchone():
            print("收藏表不存在")
            return
            
        # 查看表结构
        cursor.execute("DESCRIBE favorites")
        print("收藏表结构:")
        for col in cursor.fetchall():
            print(f"  {col[0]:20} {col[1]:15} {col[2]}")
            
        # 查看表数据
        cursor.execute("SELECT * FROM favorites LIMIT 5")
        print("\n收藏表数据（前5条）:")
        for row in cursor.fetchall():
            print(f"  {row}")
            
        cursor.close()
        conn.close()
        
        print("\n=== 检查完成 ===")
        
    except Exception as e:
        print(f"检查过程中出现错误: {e}")

if __name__ == "__main__":
    check_favorites_table()