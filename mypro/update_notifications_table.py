"""
更新通知表结构，添加detail_content和publisher字段
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine
from sqlalchemy import text

def update_notifications_table():
    """更新通知表结构"""
    print("正在更新通知表结构...")
    
    with engine.connect() as conn:
        try:
            # 检查是否已有detail_content字段
            result = conn.execute(text("SHOW COLUMNS FROM notifications LIKE 'detail_content'"))
            if not result.fetchone():
                print("添加detail_content字段...")
                conn.execute(text("ALTER TABLE notifications ADD COLUMN detail_content TEXT AFTER content"))
                conn.commit()
                print("[成功] detail_content字段添加成功")
            else:
                print("[存在] detail_content字段已存在")
            
            # 检查是否已有publisher字段
            result = conn.execute(text("SHOW COLUMNS FROM notifications LIKE 'publisher'"))
            if not result.fetchone():
                print("添加publisher字段...")
                conn.execute(text("ALTER TABLE notifications ADD COLUMN publisher VARCHAR(100) AFTER file_path"))
                conn.commit()
                print("[成功] publisher字段添加成功")
            else:
                print("[存在] publisher字段已存在")
            
            # 检查是否已有views字段
            result = conn.execute(text("SHOW COLUMNS FROM notifications LIKE 'views'"))
            if not result.fetchone():
                print("添加views字段...")
                conn.execute(text("ALTER TABLE notifications ADD COLUMN views INT DEFAULT 0 AFTER publisher"))
                conn.commit()
                print("[成功] views字段添加成功")
            else:
                print("[存在] views字段已存在")
            
            # 验证表结构
            print("\n验证表结构...")
            result = conn.execute(text("DESCRIBE notifications"))
            columns = [row[0] for row in result]
            print("当前通知表字段:", columns)
            
            required_columns = ['id', 'title', 'content', 'detail_content', 'category', 
                              'is_important', 'file_path', 'publisher', 'views', 
                              'created_at', 'updated_at']
            
            missing_columns = [col for col in required_columns if col not in columns]
            if missing_columns:
                print(f"✗ 缺少字段: {missing_columns}")
                return False
            else:
                print("[完整] 表结构完整")
                return True
                
        except Exception as e:
            print(f"[失败] 更新表结构失败: {e}")
            return False

if __name__ == "__main__":
    if update_notifications_table():
        print("\n通知表结构更新完成！")
    else:
        print("\n通知表结构更新失败！")
        sys.exit(1)