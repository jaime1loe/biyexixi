#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试提问API
"""
import sys
import io
import requests

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("测试提问API")
print("=" * 60)

BASE_URL = "http://localhost:8000"

try:
    # 1. 先登录获取token
    print("\n1. 登录获取token...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print(f"  ✓ 登录成功, token: {token[:20]}...")
    else:
        print(f"  ✗ 登录失败: {response.status_code}")
        print(f"   响应: {response.text}")
        sys.exit(1)
    
    # 2. 测试提问
    print("\n2. 测试提问API...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    question_data = {
        "question": "测试问题: ask_count字段修复后是否能正常提问？",
        "category": "测试"
    }
    
    response = requests.post(f"{BASE_URL}/api/questions/", 
                            json=question_data, 
                            headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("  ✓ 提问成功！")
        print(f"    问题ID: {result['id']}")
        print(f"    问题内容: {result['question']}")
        print(f"    提问次数: {result.get('ask_count', 'N/A')}")
        print(f"    答案: {result.get('answer', 'N/A')}")
    else:
        print(f"  ✗ 提问失败: {response.status_code}")
        print(f"   响应: {response.text}")
        
        # 如果是500错误，显示详细信息
        if response.status_code == 500:
            try:
                error_detail = response.json()
                print(f"   错误详情: {error_detail}")
            except:
                pass
    
    # 3. 测试重复提问（应该增加ask_count）
    print("\n3. 测试重复提问（应该增加ask_count）...")
    response = requests.post(f"{BASE_URL}/api/questions/", 
                            json=question_data, 
                            headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("  ✓ 重复提问成功！")
        print(f"    问题ID: {result['id']}")
        print(f"    提问次数: {result.get('ask_count', 'N/A')}")
        print(f"    ask_count 应该增加: 是")
    else:
        print(f"  ✗ 重复提问失败: {response.status_code}")
        print(f"   响应: {response.text}")
    
    # 4. 测试获取问题列表
    print("\n4. 测试获取我的问题列表...")
    response = requests.get(f"{BASE_URL}/api/questions/my", headers=headers)
    
    if response.status_code == 200:
        questions = response.json()
        print(f"  ✓ 获取成功，共 {len(questions)} 个问题")
        if questions:
            print("    最近的问题:")
            for q in questions[:3]:  # 显示前3个
                print(f"    - ID:{q['id']} {q['question'][:30]}... ask_count:{q.get('ask_count', 'N/A')}")
    else:
        print(f"  ✗ 获取问题列表失败: {response.status_code}")
        print(f"   响应: {response.text}")
    
    # 5. 测试热门问题统计
    print("\n5. 测试热门问题统计...")
    response = requests.get(f"{BASE_URL}/api/statistics/top-questions")
    
    if response.status_code == 200:
        top_questions = response.json()
        print(f"  ✓ 获取成功，共 {len(top_questions)} 个热门问题")
        if top_questions:
            print("    热门问题排名:")
            for i, q in enumerate(top_questions[:5], 1):  # 显示前5个
                print(f"    {i}. ask_count:{q.get('ask_count', 1)} - {q['question'][:30]}...")
    else:
        print(f"  ✗ 获取热门问题失败: {response.status_code}")
        print(f"   响应: {response.text}")
    
    print("\n" + "=" * 60)
    print("API测试完成！")
    print("=" * 60)
    
except requests.exceptions.ConnectionError:
    print("\n[错误] 无法连接到后端服务器")
    print("请确认后端服务已启动在 http://localhost:8000")
    print("启动命令: cd d:\\毕业设计\\backend && python main.py")
    sys.exit(1)
except Exception as e:
    print(f"\n[错误] 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)