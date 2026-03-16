import requests
import json

BASE_URL = "http://localhost:8000"

# 简单的DELETE路由测试
def test_delete_directly():
    # 登录
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "test_delete_user",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print("登录失败")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 获取我的申请
    my_response = requests.get(
        f"{BASE_URL}/api/profile-changes/my-requests",
        headers=headers
    )
    
    if my_response.status_code == 200:
        requests_list = my_response.json()
        print(f"我的申请数量: {len(requests_list)}")
        
        if requests_list:
            request_id = requests_list[0]["id"]
            print(f"尝试删除申请 ID: {request_id}")
            print(f"申请状态: {requests_list[0]['status']}")
            
            # 测试DELETE请求
            print(f"\n测试 DELETE /api/profile-changes/{request_id}")
            delete_response = requests.delete(
                f"{BASE_URL}/api/profile-changes/{request_id}",
                headers=headers
            )
            print(f"状态码: {delete_response.status_code}")
            print(f"响应内容: {delete_response.text}")
            
            # 检查路由文档
            print(f"\n检查所有可用的profile-changes路由...")
            try:
                openapi = requests.get(f"{BASE_URL}/openapi.json")
                if openapi.status_code == 200:
                    paths = openapi.json()["paths"]
                    for path, methods in paths.items():
                        if "profile-changes" in path:
                            print(f"  路径: {path}")
                            for method in methods.keys():
                                print(f"    方法: {method.upper()}")
            except:
                pass

if __name__ == "__main__":
    test_delete_directly()
