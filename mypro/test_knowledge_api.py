"""
测试知识库API
"""
import sys
import os
import requests

BASE_URL = "http://localhost:8000/api"

def test_knowledge_api():
    """测试知识库API"""
    print("测试知识库API...")

    try:
        # 测试获取知识列表
        print("\n1. 测试 GET /api/knowledge/")
        response = requests.get(f"{BASE_URL}/knowledge/", params={
            "skip": 0,
            "limit": 10
        })
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回数据: {len(data)} 条记录")
            if data:
                print(f"   第一条数据: {data[0]}")
        else:
            print(f"   错误信息: {response.text}")

        # 测试获取分类
        print("\n2. 测试 GET /api/knowledge/categories")
        response = requests.get(f"{BASE_URL}/knowledge/categories")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回数据: {data}")

        print("\n测试完成!")

    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")

if __name__ == "__main__":
    test_knowledge_api()
