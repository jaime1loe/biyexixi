"""测试实际HTTP请求"""
import requests
import json

# 1. 尝试不登录直接访问（应该401）
print("=== 测试1: 未认证访问 ===")
response = requests.get("http://localhost:8000/api/course-selection/available")
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:100]}")

# 2. 创建一个临时的测试用户token（通过直接调用）
print("\n=== 测试2: 创建测试token ===")
from app.utils import create_access_token
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
student = db.query(User).filter(User.role == "student").first()

if student:
    token = create_access_token(data={"sub": str(student.id)})
    print(f"创建token成功: {token[:30]}...")

    # 3. 使用这个token访问API
    print("\n=== 测试3: 使用token访问API ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"成功！返回 {len(data)} 门课程")
        if data:
            print(f"第一门: {data[0]['course_name']}")
    else:
        print(f"失败: {response.text}")

else:
    print("没有找到学生用户")

db.close()
