"""
添加知识库审核相关字段到数据库
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import text
from app.database import engine

def add_review_fields():
    """添加审核相关字段"""
    with engine.connect() as conn:
        try:
            # 检查uploader_id字段是否存在
            result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'uploader_id'"))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN uploader_id INT COMMENT '上传者用户ID'"))
                print("已添加 uploader_id 字段")
            else:
                print("uploader_id 字段已存在")

            # 检查reviewer_id字段是否存在
            result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'reviewer_id'"))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN reviewer_id INT COMMENT '审核人用户ID'"))
                print("已添加 reviewer_id 字段")
            else:
                print("reviewer_id 字段已存在")

            # 检查review_status字段是否存在
            result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'review_status'"))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN review_status VARCHAR(20) DEFAULT 'pending' COMMENT '审核状态: pending=待审核, approved=已通过, rejected=已拒绝'"))
                print("已添加 review_status 字段")
            else:
                print("review_status 字段已存在")

            # 检查rejection_reason字段是否存在
            result = conn.execute(text("SHOW COLUMNS FROM knowledge LIKE 'rejection_reason'"))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE knowledge ADD COLUMN rejection_reason TEXT COMMENT '拒绝原因'"))
                print("已添加 rejection_reason 字段")
            else:
                print("rejection_reason 字段已存在")

            # 提交更改
            conn.commit()
            print("\n数据库字段添加成功！")

        except Exception as e:
            conn.rollback()
            print(f"\n添加字段失败: {e}")

if __name__ == "__main__":
    add_review_fields()
