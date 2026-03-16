"""
测试个人资料修改申请的删除功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 测试删除功能 - 需要一个有效的token
# 使用管理员账号进行测试
def test_delete_pending_request():
    # 首先登录获取token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        # 登录
        print("1. 尝试登录...")
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"登录响应状态码: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.text}")
            return
            
        token = login_response.json()["access_token"]
        print(f"登录成功，获取到token: {token[:20]}...")
        
        # 获取待审核的申请
        headers = {"Authorization": f"Bearer {token}"}
        print("\n2. 获取待审核的申请...")
        
        # 先尝试获取所有申请
        all_requests = requests.get(f"{BASE_URL}/api/profile-changes/all", headers=headers)
        print(f"获取所有申请状态码: {all_requests.status_code}")
        
        if all_requests.status_code == 200:
            requests_list = all_requests.json()
            print(f"所有申请数量: {len(requests_list)}")
            
            # 找到待审核的申请
            pending_requests = [r for r in requests_list if r["status"] == "pending"]
            print(f"待审核申请数量: {len(pending_requests)}")
            
            if pending_requests:
                request_id = pending_requests[0]["id"]
                print(f"\n3. 尝试删除申请 ID {request_id}...")
                
                # 检查这个申请是否属于当前用户
                user_id = pending_requests[0]["user_id"]
                print(f"申请属于用户 ID: {user_id}")
                
                # 尝试删除
                delete_response = requests.delete(f"{BASE_URL}/api/profile-changes/{request_id}", headers=headers)
                print(f"删除响应状态码: {delete_response.status_code}")
                print(f"删除响应内容: {delete_response.text}")
                
                if delete_response.status_code == 200:
                    print("✓ 删除成功！")
                else:
                    print(f"✗ 删除失败")
            else:
                print("没有找到待审核的申请")
        else:
            print(f"获取申请失败: {all_requests.text}")
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_delete_pending_request()
