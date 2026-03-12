"""
将爬取的数据导入到数据库
"""

import json
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Knowledge
from datetime import datetime


def import_knowledge_from_json(json_file: str):
    """从 JSON 文件导入知识库数据"""

    # 读取 JSON 文件
    print(f"正在读取文件: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"共读取 {len(data)} 条数据")

    # 创建数据库会话
    db = SessionLocal()

    try:
        imported_count = 0
        skipped_count = 0

        for item in data:
            try:
                # 检查是否已存在（根据标题）
                existing = db.query(Knowledge).filter(
                    Knowledge.title == item.get('title', '')
                ).first()

                if existing:
                    print(f"跳过已存在: {item.get('title', '')[:50]}...")
                    skipped_count += 1
                    continue

                # 创建新记录
                knowledge = Knowledge(
                    title=item.get('title', '')[:200],  # 限制长度
                    content=item.get('content', ''),
                    category=item.get('category', '校园资讯'),
                    tags=item.get('tags', ''),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )

                db.add(knowledge)
                imported_count += 1

                if imported_count % 10 == 0:
                    db.commit()
                    print(f"已导入 {imported_count} 条...")

            except Exception as e:
                print(f"导入单条数据失败: {e}")
                db.rollback()
                continue

        # 提交所有更改
        db.commit()

        print(f"\n" + "=" * 60)
        print(f"导入完成！")
        print(f"成功导入: {imported_count} 条")
        print(f"跳过重复: {skipped_count} 条")
        print(f"=" * 60)

    except Exception as e:
        print(f"导入过程出错: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """主函数"""
    json_file = 'd:/毕业设计/wust_knowledge_data.json'

    if not os.path.exists(json_file):
        print(f"错误: 文件不存在 {json_file}")
        print("请先运行 crawl_wust.py 生成数据")
        return

    import_knowledge_from_json(json_file)


if __name__ == '__main__':
    main()
