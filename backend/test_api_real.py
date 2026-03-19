"""测试API - 使用实际用户"""
import requests

# 用admin登录
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "admin", "password": "admin"}
)

print(f"登录状态: {login_response.status_code}")
if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Token获取成功: {token[:20]}...")

    headers = {"Authorization": f"Bearer {token}"}

    # 测试可选课程API（admin会被拒绝，但能看到错误信息）
    available_response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )
    print(f"\n可选课程API状态: {available_response.status_code}")
    print(f"响应: {available_response.text[:200]}")
