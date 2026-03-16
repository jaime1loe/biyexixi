"""
测试profile_changes API
"""
import sys
import io
from pathlib import Path

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_auth_login():
    """测试登录获取token"""
    print("=" * 60)
    print("测试登录")
    print("=" * 60)

    login_data = {
        "username": "admin",
        "password": "admin123456"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✓ 登录成功")
            print(f"Token: {token[:50]}...")
            return token
        else:
            print(f"✗ 登录失败")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return None

def test_get_current_user(token):
    """测试获取当前用户信息"""
    print("\n" + "=" * 60)
    print("测试获取当前用户信息")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取成功")
            print(f"用户名: {data.get('username')}")
            print(f"角色: {data.get('role')}")
            print(f"邮箱: {data.get('email')}")
            return data
        else:
            print(f"✗ 获取失败")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return None

def test_submit_profile_change(token):
    """测试提交个人信息修改申请"""
    print("\n" + "=" * 60)
    print("测试提交个人信息修改申请")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    change_data = {
        "real_name": "管理员用户",
        "email": "admin@test.com",
        "phone": "13800138000",
        "department": "计算机学院",
        "major": "计算机科学与技术",
        "bio": "这是个人简介",
        "reason": "测试提交修改申请"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/profile-changes/submit", json=change_data, headers=headers)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 提交成功")
            print(f"申请ID: {data.get('id')}")
            print(f"状态: {data.get('status')}")
            return data
        else:
            print(f"✗ 提交失败")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return None

def test_get_my_requests(token):
    """测试获取我的修改申请记录"""
    print("\n" + "=" * 60)
    print("测试获取我的修改申请记录")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{BASE_URL}/api/profile-changes/my-requests", headers=headers)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取成功")
            print(f"记录数: {len(data)}")
            for req in data:
                print(f"  - ID: {req.get('id')}, 状态: {req.get('status')}, 原因: {req.get('reason')}")
            return data
        else:
            print(f"✗ 获取失败")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return None

def main():
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  profile_changes API 测试".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)

    # 1. 登录获取token
    token = test_auth_login()
    if not token:
        print("\n✗ 无法获取token，测试终止")
        return

    # 2. 获取当前用户信息
    user_data = test_get_current_user(token)

    # 3. 提交修改申请
    change_data = test_submit_profile_change(token)

    # 4. 获取我的申请记录
    requests_data = test_get_my_requests(token)

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
