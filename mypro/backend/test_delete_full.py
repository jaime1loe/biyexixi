"""
直接测试删除路由 - 使用用户ID 1的token
需要先获取有效的token
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

# 提供一个token用于测试（需要用户提供）
# 或者我们可以尝试重置密码
def test_with_test_token():
    """
    由于不知道正确的密码，我们尝试创建一个测试用户
    """
    
    # 尝试注册新用户
    register_data = {
        "username": "test_delete_user",
        "password": "123456",
        "email": "test@test.com"
    }
    
    try:
        print("1. 尝试注册测试用户...")
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"注册响应状态码: {register_response.status_code}")
        
        if register_response.status_code in [200, 201]:
            print("注册成功")
            
            # 登录
            print("\n2. 登录测试用户...")
            login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "username": "test_delete_user",
                "password": "123456"
            })
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                print(f"登录成功，获取到token: {token[:20]}...")
                
                # 提交一个修改申请
                print("\n3. 提交测试修改申请...")
                submit_response = requests.post(
                    f"{BASE_URL}/api/profile-changes/submit",
                    headers={"Authorization": f"Bearer {token}"},
                    json={
                        "real_name": "测试修改",
                        "reason": "测试删除功能"
                    }
                )
                print(f"提交申请状态码: {submit_response.status_code}")
                
                if submit_response.status_code == 200:
                    request_data = submit_response.json()
                    request_id = request_data["id"]
                    print(f"申请提交成功，ID: {request_id}")
                    
                    # 获取我的申请
                    print("\n4. 获取我的申请...")
                    my_requests = requests.get(
                        f"{BASE_URL}/api/profile-changes/my-requests",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    print(f"获取申请状态码: {my_requests.status_code}")
                    
                    if my_requests.status_code == 200:
                        requests_list = my_requests.json()
                        print(f"我的申请数量: {len(requests_list)}")
                    
                    # 尝试删除申请
                    print(f"\n5. 尝试删除申请 ID {request_id}...")
                    delete_response = requests.delete(
                        f"{BASE_URL}/api/profile-changes/{request_id}",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    print(f"删除响应状态码: {delete_response.status_code}")
                    print(f"删除响应内容: {delete_response.text}")
                    
                    if delete_response.status_code == 200:
                        print("✓ 删除成功！")
                    else:
                        print("✗ 删除失败")
                else:
                    print(f"提交申请失败: {submit_response.text}")
            else:
                print(f"登录失败: {login_response.text}")
        else:
            print(f"注册失败: {register_response.text}")
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_test_token()
