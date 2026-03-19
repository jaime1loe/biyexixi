"""使用testuser测试API"""
import requests

# 用testuser登录
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"username": "testuser", "password": "testuser"}
)

print(f"登录状态: {login_response.status_code}")
if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"Token获取成功")

    headers = {"Authorization": f"Bearer {token}"}

    # 测试可选课程API
    available_response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )
    print(f"\n可选课程API状态: {available_response.status_code}")
    if available_response.status_code == 200:
        data = available_response.json()
        print(f"返回课程数量: {len(data)}")
        if data:
            first = data[0]
            print(f"第一门课程: {first['course_name']}")
            print(f"容量: {first.get('capacity', 'N/A')}, 剩余: {first.get('remaining_count', 'N/A')}")
    else:
        print(f"错误内容: {available_response.text}")
else:
    print(f"登录失败: {login_response.text}")
