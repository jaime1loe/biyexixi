import requests
import sys

BASE_URL = "http://localhost:8000"

try:
    # 测试获取问题列表
    print("测试 GET /api/questions/ ...")
    response = requests.get(f"{BASE_URL}/api/questions/", params={"skip": 0, "limit": 10})
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"成功! 获取到 {len(data)} 条问题")
    else:
        print(f"错误: {response.text}")
except Exception as e:
    print(f"请求失败: {e}")
