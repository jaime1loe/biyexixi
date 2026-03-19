"""验证退选行为"""
import requests
from app.database import SessionLocal
from app.models import User, Course, CourseSelection
from app.utils import create_access_token

db = SessionLocal()

student = db.query(User).filter(User.role == "student").first()
course = db.query(Course).first()

print(f"学生: {student.username}")
print(f"课程: {course.course_name}")

token = create_access_token(data={"sub": str(student.id)})
headers = {"Authorization": f"Bearer {token}"}

# 选课
print("\n[1] 选课...")
select_data = {"course_id": course.id, "semester": "2024-2025-2"}
response = requests.post("http://localhost:8000/api/course-selection/select",
                       headers=headers, json=select_data)

if response.status_code == 200:
    selection = response.json()
    print(f"[OK] 选课成功，ID: {selection['id']}, 状态: {selection['status']}")
    selection_id = selection['id']
else:
    print(f"[FAIL] {response.text}")
    exit(1)

# 查询我的选课（默认显示所有状态）
print("\n[2] 查询我的选课（全部状态）...")
response = requests.get("http://localhost:8000/api/course-selection/my-courses",
                      headers=headers)

if response.status_code == 200:
    selections = response.json()
    print(f"获取到 {len(selections)} 条记录")
    for sel in selections:
        print(f"  ID: {sel['id']}, 课程: {sel['course_name']}, 状态: {sel['status']}")

# 只查询已选的课程
print("\n[3] 查询我的选课（只看已选）...")
response = requests.get("http://localhost:8000/api/course-selection/my-courses?status=selected",
                      headers=headers)

if response.status_code == 200:
    selected_courses = response.json()
    print(f"获取到 {len(selected_courses)} 条已选记录")

# 退选
print("\n[4] 退选...")
response = requests.delete(f"http://localhost:8000/api/course-selection/{selection_id}",
                         headers=headers)

if response.status_code == 200:
    print(f"[OK] 退选成功")
else:
    print(f"[FAIL] {response.text}")

# 再次查询
print("\n[5] 再次查询我的选课（全部状态）...")
response = requests.get("http://localhost:8000/api/course-selection/my-courses",
                      headers=headers)

if response.status_code == 200:
    selections = response.json()
    print(f"获取到 {len(selections)} 条记录")
    for sel in selections:
        print(f"  ID: {sel['id']}, 课程: {sel['course_name']}, 状态: {sel['status']}")

# 再次查询已选的课程
print("\n[6] 再次查询我的选课（只看已选）...")
response = requests.get("http://localhost:8000/api/course-selection/my-courses?status=selected",
                      headers=headers)

if response.status_code == 200:
    selected_courses = response.json()
    print(f"获取到 {len(selected_courses)} 条已选记录")

# 清理
db.query(CourseSelection).filter(CourseSelection.student_id == student.id).delete()
db.commit()

db.close()
print("\n[OK] 测试完成!")
