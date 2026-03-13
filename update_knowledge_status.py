#!/usr/bin/env python3
"""更新knowledge记录的审核状态"""

from backend.app.database import engine
from sqlalchemy import text

def main():
    print("更新knowledge记录的审核状态...")
    
    with engine.connect() as conn:
        # 将所有pending状态的知识改为approved状态
        result = conn.execute(
            text("UPDATE knowledge SET review_status = 'approved' WHERE review_status = 'pending'")
        )
        conn.commit()
        
        print(f"已更新 {result.rowcount} 条记录的审核状态")
        
        # 验证更新结果
        result = conn.execute(text("SELECT review_status, COUNT(*) FROM knowledge GROUP BY review_status"))
        print("\n更新后的审核状态分布:")
        for row in result:
            print(f"  {row[0]}: {row[1]} 条")
        
        # 测试API是否正常工作
        print("\n测试API...")
        import requests
        response = requests.get("http://localhost:8000/api/knowledge/?skip=0&limit=10")
        print(f"知识列表API状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"成功获取知识: {len(data)} 条")
            if data:
                print("前3条知识:")
                for i, item in enumerate(data[:3]):
                    print(f"  {i+1}. {item['title']}")

if __name__ == "__main__":
    main()