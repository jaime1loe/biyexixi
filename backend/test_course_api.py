"""测试course-selection API"""
import requests

# 先登录获取token
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "student1", "password": "password"}
)

print(f"登录状态: {login_response.status_code}")
if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Token: {token[:20]}...")

    # 测试可选课程API
    headers = {"Authorization": f"Bearer {token}"}
    available_response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )
    print(f"\n可选课程API状态: {available_response.status_code}")
    if available_response.status_code == 200:
        data = available_response.json()
        print(f"返回课程数量: {len(data)}")
        if data:
            print(f"第一门课程: {data[0]['course_name']}")
    else:
        print(f"错误: {available_response.text}")
else:
    print(f"登录失败: {login_response.text}")
