# -*- coding: utf-8 -*-
"""
检查后端服务的详细错误信息
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("检查后端服务状态")
print("=" * 60)
print()

# 1. 检查后端是否运行
print("1. 检查后端服务是否运行...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("   [OK] 后端服务正在运行")
        print("   响应:", response.json())
    else:
        print(f"   [ERROR] 后端服务响应异常: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] 无法连接后端: {e}")
    sys.exit(1)
print()

# 2. 检查所有profile-changes路由
print("2. 检查所有profile-changes路由...")
try:
    response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
    if response.status_code == 200:
        openapi = response.json()
        paths = openapi.get("paths", {})

        profile_routes = []
        for path, methods in paths.items():
            if "profile-changes" in path:
                for method in methods.keys():
                    profile_routes.append(f"{method.upper()} {path}")

        print(f"   找到 {len(profile_routes)} 个profile-changes路由:")
        for route in sorted(profile_routes):
            print(f"   - {route}")

        # 检查是否有DELETE路由
        has_delete = any("DELETE" in route for route in profile_routes)
        if has_delete:
            print("\n   [OK] DELETE路由存在")
        else:
            print("\n   [ERROR] DELETE路由不存在 - 需要重启后端服务！")
    else:
        print(f"   [ERROR] 获取OpenAPI文档失败: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] 检查路由失败: {e}")
print()

# 3. 测试登录
print("3. 测试登录功能...")
try:
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "test_delete_user", "password": "123456"},
        timeout=5
    )
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print("   [OK] 登录成功")
        print(f"   Token: {token[:30]}...")

        # 4. 测试获取我的申请
        print("\n4. 测试获取我的申请...")
        headers = {"Authorization": f"Bearer {token}"}
        my_response = requests.get(
            f"{BASE_URL}/api/profile-changes/my-requests",
            headers=headers,
            timeout=5
        )

        if my_response.status_code == 200:
            requests_list = my_response.json()
            print(f"   [OK] 获取成功，找到 {len(requests_list)} 个申请")

            if requests_list:
                request_id = requests_list[0]["id"]
                status = requests_list[0]["status"]
                print(f"   第一个申请: ID={request_id}, Status={status}")

                # 5. 测试DELETE请求
                print(f"\n5. 测试DELETE请求...")
                print(f"   发送: DELETE {BASE_URL}/api/profile-changes/{request_id}")

                delete_response = requests.delete(
                    f"{BASE_URL}/api/profile-changes/{request_id}",
                    headers=headers,
                    timeout=5
                )

                print(f"   响应状态码: {delete_response.status_code}")

                if delete_response.status_code == 200:
                    print("   [OK] 删除成功!")
                    print("   响应:", delete_response.json())
                elif delete_response.status_code == 404:
                    print("   [ERROR] 404错误 - DELETE路由未注册")
                    print("   响应:", delete_response.text)
                elif delete_response.status_code == 403:
                    print("   [ERROR] 403错误 - 无权删除")
                    print("   响应:", delete_response.text)
                elif delete_response.status_code == 400:
                    print("   [ERROR] 400错误 - 请求参数错误")
                    print("   响应:", delete_response.text)
                else:
                    print("   [ERROR] 其他错误")
                    print("   响应:", delete_response.text)
            else:
                print("   没有待删除的申请")
        else:
            print(f"   [ERROR] 获取申请失败: {my_response.status_code}")
            print("   响应:", my_response.text)
    else:
        print(f"   [ERROR] 登录失败: {login_response.status_code}")
        print("   响应:", login_response.text)
except Exception as e:
    print(f"   [ERROR] 测试失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("检查完成")
print("=" * 60)
