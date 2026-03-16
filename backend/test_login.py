"""
测试登录接口
"""
import requests

def test_login(username, password):
    """测试登录"""
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=data)
        print(f"测试账号: {username} / {password}")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        print("-" * 60)
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == '__main__':
    test_login("admin", "admin123")
    test_login("teacher", "teacher123")
    test_login("student1", "student123")
