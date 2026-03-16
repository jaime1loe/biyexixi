"""测试各个API接口"""
import requests

BASE_URL = "http://localhost:8000"

print("测试API接口...")
print("=" * 50)

# 1. 测试健康检查
print("\n1. 测试健康检查")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
except Exception as e:
    print(f"   错误: {e}")

# 2. 测试统计概览
print("\n2. 测试统计概览")
try:
    response = requests.get(f"{BASE_URL}/api/statistics/overview")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   错误: {e}")

# 3. 测试热门问题
print("\n3. 测试热门问题")
try:
    response = requests.get(f"{BASE_URL}/api/statistics/top-questions?limit=5")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   错误: {e}")

# 4. 测试通知列表
print("\n4. 测试通知列表")
try:
    response = requests.get(f"{BASE_URL}/api/notifications/")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   错误: {e}")

# 5. 测试问题列表
print("\n5. 测试问题列表")
try:
    response = requests.get(f"{BASE_URL}/api/questions/")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   错误: {e}")

# 6. 测试知识库列表
print("\n6. 测试知识库列表")
try:
    response = requests.get(f"{BASE_URL}/api/knowledge/")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   错误: {e}")

print("\n" + "=" * 50)
print("测试完成!")
