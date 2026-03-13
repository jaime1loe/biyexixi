#!/usr/bin/env python3
"""修复knowledge表缺少字段的问题"""

from backend.app.database import engine
from sqlalchemy import text

def check_knowledge_table():
    """检查knowledge表结构"""
    print("检查knowledge表结构...")
    
    with engine.connect() as conn:
        # 检查表结构
        result = conn.execute(text("DESCRIBE knowledge"))
        fields = [row[0] for row in result]
        print("当前字段:", fields)
        
        # 检查是否缺少status字段
        if 'status' not in fields:
            print("发现缺失字段: status")
            return False, fields
        
        return True, fields

def fix_knowledge_table():
    """修复knowledge表结构"""
    print("\n修复knowledge表结构...")
    
    with engine.connect() as conn:
        # 检查并添加缺失的字段
        missing_fields = []
        
        # 检查status字段
        result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'status'"))
        if not result.fetchone():
            missing_fields.append("status")
            print("需要添加status字段")
        
        # 检查uploader_id字段
        result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'uploader_id'"))
        if not result.fetchone():
            missing_fields.append("uploader_id")
            print("需要添加uploader_id字段")
        
        # 检查reviewer_id字段
        result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'reviewer_id'"))
        if not result.fetchone():
            missing_fields.append("reviewer_id")
            print("需要添加reviewer_id字段")
        
        # 检查review_status字段
        result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'review_status'"))
        if not result.fetchone():
            missing_fields.append("review_status")
            print("需要添加review_status字段")
        
        # 检查rejection_reason字段
        result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'rejection_reason'"))
        if not result.fetchone():
            missing_fields.append("rejection_reason")
            print("需要添加rejection_reason字段")
        
        # 添加缺失字段
        for field in missing_fields:
            if field == "status":
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"))
                print(f"已添加字段: {field}")
            elif field == "uploader_id":
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN uploader_id INT"))
                print(f"已添加字段: {field}")
            elif field == "reviewer_id":
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN reviewer_id INT"))
                print(f"已添加字段: {field}")
            elif field == "review_status":
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN review_status VARCHAR(20) DEFAULT 'pending'"))
                print(f"已添加字段: {field}")
            elif field == "rejection_reason":
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN rejection_reason TEXT"))
                print(f"已添加字段: {field}")
        
        conn.commit()
        
        if missing_fields:
            print(f"\n成功添加 {len(missing_fields)} 个缺失字段")
        else:
            print("\n表结构完整，无需修复")

def update_existing_records():
    """更新现有记录的字段值"""
    print("\n更新现有记录...")
    
    with engine.connect() as conn:
        # 为现有记录设置默认值
        conn.execute(text("UPDATE knowledge SET status = 'completed' WHERE status IS NULL"))
        conn.execute(text("UPDATE knowledge SET review_status = 'approved' WHERE review_status IS NULL"))
        conn.commit()
        
        result = conn.execute(text("SELECT COUNT(*) FROM knowledge"))
        count = result.fetchone()[0]
        print(f"已更新 {count} 条记录的字段值")

def main():
    print("开始修复knowledge表...")
    
    # 检查表结构
    is_ok, fields = check_knowledge_table()
    
    if not is_ok:
        # 修复表结构
        fix_knowledge_table()
        
        # 更新现有记录
        update_existing_records()
        
        # 再次检查
        print("\n修复后检查:")
        check_knowledge_table()
    
    print("\n修复完成!")

if __name__ == "__main__":
    main()