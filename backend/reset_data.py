#!/usr/bin/env python
"""
重置数据库数据
"""
from sqlalchemy import text
from app.database import engine


def reset_database():
    """重置数据库表数据"""
    tables = ['feedbacks', 'questions', 'knowledge', 'users', 'statistics']
    
    print("⚠ 警告：即将删除所有数据！")
    confirm = input("确认继续？(yes/no): ")
    
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    try:
        with engine.connect() as conn:
            # 禁用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            for table in tables:
                conn.execute(text(f"TRUNCATE TABLE {table}"))
                print(f"✓ 已清空表: {table}")
            
            # 启用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            conn.commit()
        
        print("\n✓ 数据库重置完成")
        print("\n现在可以运行 'python init_data.py' 来重新初始化数据")
    except Exception as e:
        print(f"✗ 重置失败: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("重置数据库")
    print("=" * 50)
    reset_database()
