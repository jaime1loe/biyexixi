import requests
import json

BASE_URL = "http://localhost:8000"

def test_direct_delete():
    """直接向后端发送DELETE请求"""
    # 先登录获取token
    print("1. 登录获取token...")
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "test_delete_user",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    print(f"登录成功")
    
    # 获取我的申请
    print("\n2. 获取我的申请...")
    headers = {"Authorization": f"Bearer {token}"}
    my_response = requests.get(
        f"{BASE_URL}/api/profile-changes/my-requests",
        headers=headers
    )
    
    if my_response.status_code == 200:
        requests_list = my_response.json()
        if requests_list:
            request_id = requests_list[0]["id"]
            print(f"找到申请 ID: {request_id}, 状态: {requests_list[0]['status']}")
            
            # 直接向后端发送DELETE请求
            print(f"\n3. 直接向后端发送 DELETE /api/profile-changes/{request_id}...")
            delete_response = requests.delete(
                f"{BASE_URL}/api/profile-changes/{request_id}",
                headers=headers
            )
            
            print(f"状态码: {delete_response.status_code}")
            print(f"响应头: {dict(delete_response.headers)}")
            print(f"响应内容: {delete_response.text}")
            
            if delete_response.status_code == 200:
                print("\n删除成功！")
            elif delete_response.status_code == 404:
                print("\n404错误 - DELETE路由不存在！")
            else:
                print(f"\n其他错误: {delete_response.status_code}")
        else:
            print("没有找到待删除的申请")
    else:
        print(f"获取申请失败: {my_response.text}")

if __name__ == "__main__":
    test_direct_delete()
