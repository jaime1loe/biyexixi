import sys
import io
import requests

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("测试认证API")
print("=" * 60)

BASE_URL = "http://localhost:8000"

try:
    # 1. 测试登录
    print("\n1. 测试登录接口...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

    if response.status_code == 200:
        print("   ✓ 登录成功")
        token_data = response.json()
        token = token_data["access_token"]
        print(f"   Token: {token[:20]}...")
    else:
        print(f"   ✗ 登录失败: {response.status_code}")
        print(f"   响应: {response.text}")
        sys.exit(1)

    # 2. 测试获取当前用户信息
    print("\n2. 测试获取当前用户信息...")
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)

    if response.status_code == 200:
        print("   ✓ 获取用户信息成功")
        user_info = response.json()
        print(f"   用户ID: {user_info['id']}")
        print(f"   用户名: {user_info['username']}")
        print(f"   角色: {user_info['role']}")
        print(f"   邮箱: {user_info.get('email', 'N/A')}")
    else:
        print(f"   ✗ 获取用户信息失败: {response.status_code}")
        print(f"   响应: {response.text}")

    # 3. 测试其他用户登录
    print("\n3. 测试其他用户登录...")
    test_users = [
        ("teacher", "123456"),
        ("student1", "123456")
    ]

    for username, password in test_users:
        login_data = {"username": username, "password": password}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

        if response.status_code == 200:
            print(f"   ✓ {username} 登录成功")

            # 测试获取用户信息
            token_data = response.json()
            token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            user_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            if user_response.status_code == 200:
                user_info = user_response.json()
                print(f"     - 角色: {user_info['role']}, 真实姓名: {user_info.get('real_name', 'N/A')}")
            else:
                print(f"     ✗ 获取用户信息失败")
        else:
            print(f"   ✗ {username} 登录失败")

    print("\n" + "=" * 60)
    print("API测试完成")
    print("=" * 60)

except requests.exceptions.ConnectionError:
    print("\n[错误] 无法连接到后端服务器")
    print("请确认后端服务已启动在 http://localhost:8000")
    sys.exit(1)
except Exception as e:
    print(f"\n[错误] 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
