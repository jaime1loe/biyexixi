"""
测试前端API调用
"""
import sys
import io

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("=" * 60)
    print("测试后端API端点")
    print("=" * 60)

    # 1. 测试登录（已知密码）
    print("\n1. 测试登录...")
    login_data = {
        "username": "admin",
        "password": "12345678"  # 使用更简单的密码
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.text[:200]}")

    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"   [OK] 登录成功，Token: {token[:30]}...")

        # 2. 测试获取当前用户
        print("\n2. 测试获取当前用户...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text[:200]}")

        # 3. 测试获取修改申请记录
        print("\n3. 测试获取修改申请记录...")
        response = requests.get(f"{BASE_URL}/api/profile-changes/my-requests", headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text[:200]}")

        # 4. 测试提交修改申请
        print("\n4. 测试提交修改申请...")
        change_data = {
            "real_name": "测试用户",
            "email": "test@test.com",
            "phone": "13800138000",
            "department": "计算机学院",
            "major": "计算机",
            "bio": "测试简介",
            "reason": "测试原因"
        }
        response = requests.post(f"{BASE_URL}/api/profile-changes/submit", json=change_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text[:200]}")

    else:
        # 尝试其他密码
        print("\n尝试其他密码...")
        passwords = ["admin123456", "admin", "password"]
        for pwd in passwords:
            login_data["password"] = pwd
            response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if response.status_code == 200:
                print(f"   [OK] 找到正确密码: {pwd}")
                break
            else:
                print(f"   密码 '{pwd}' 失败")

if __name__ == "__main__":
    try:
        test_endpoints()
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
