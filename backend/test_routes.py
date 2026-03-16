import requests
import json

BASE_URL = "http://localhost:8000"

# 测试所有profile-changes路由
def test_all_routes():
    # 先获取token
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "test_delete_user",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print("登录失败，请先运行test_delete_full.py注册测试用户")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("测试所有profile-changes路由:\n")
    
    # 1. 测试提交申请
    print("1. POST /api/profile-changes/submit")
    submit_response = requests.post(
        f"{BASE_URL}/api/profile-changes/submit",
        headers=headers,
        json={"reason": "测试路由"}
    )
    print(f"   状态码: {submit_response.status_code}")
    
    if submit_response.status_code == 200:
        request_id = submit_response.json()["id"]
        
        # 2. 测试获取我的申请
        print(f"\n2. GET /api/profile-changes/my-requests")
        my_response = requests.get(
            f"{BASE_URL}/api/profile-changes/my-requests",
            headers=headers
        )
        print(f"   状态码: {my_response.status_code}")
        
        # 3. 测试删除申请 - 使用不同的URL格式
        print(f"\n3. 尝试DELETE请求（不同URL格式）:")
        
        # 方式1: /api/profile-changes/{id}
        print(f"   a) DELETE /api/profile-changes/{request_id}")
        delete1 = requests.delete(
            f"{BASE_URL}/api/profile-changes/{request_id}",
            headers=headers
        )
        print(f"      状态码: {delete1.status_code}")
        print(f"      响应: {delete1.text[:200]}")
        
        # 方式2: 检查是否有其他URL格式
        print(f"\n   b) DELETE /api/profile-changes/delete/{request_id}")
        delete2 = requests.delete(
            f"{BASE_URL}/api/profile-changes/delete/{request_id}",
            headers=headers
        )
        print(f"      状态码: {delete2.status_code}")
        print(f"      响应: {delete2.text[:200]}")
        
        # 方式3: 带query参数
        print(f"\n   c) DELETE /api/profile-changes/?id={request_id}")
        delete3 = requests.delete(
            f"{BASE_URL}/api/profile-changes/",
            headers=headers,
            params={"id": request_id}
        )
        print(f"      状态码: {delete3.status_code}")
        print(f"      响应: {delete3.text[:200]}")

if __name__ == "__main__":
    test_all_routes()
