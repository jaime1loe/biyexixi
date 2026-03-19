"""测试没有成绩记录的退选功能"""
import requests
from app.database import SessionLocal
from app.models import User, Course, CourseSelection, Grade
from app.utils import create_access_token

print("测试没有成绩记录的退选功能")
print("=" * 60)

db = SessionLocal()

# 获取一个学生和一个没有成绩的课程
student = db.query(User).filter(User.role == "student").first()

# 找一个没有成绩的课程
courses_with_no_grade = db.query(Course).outerjoin(Grade).filter(Grade.id.is_(None)).first()

if not student or not courses_with_no_grade:
    print("没有找到测试数据")
    db.close()
    exit(1)

print(f"学生: {student.username}")
print(f"课程: {courses_with_no_grade.course_name} (ID: {courses_with_no_grade.id})")

# 创建token
token = create_access_token(data={"sub": str(student.id)})
headers = {"Authorization": f"Bearer {token}"}

# 选课
print("\n[1] 选课...")
select_data = {
    "course_id": courses_with_no_grade.id,
    "semester": "2024-2025-2"
}

response = requests.post(
    "http://localhost:8000/api/course-selection/select",
    headers=headers,
    json=select_data
)

if response.status_code == 200:
    selection = response.json()
    print(f"[OK] 选课成功，ID: {selection['id']}")
    selection_id = selection['id']
else:
    print(f"[FAIL] 选课失败: {response.text}")
    db.close()
    exit(1)

# 退选
print("\n[2] 退选...")
response = requests.delete(
    f"http://localhost:8000/api/course-selection/{selection_id}",
    headers=headers
)

if response.status_code == 200:
    print(f"[OK] 退选成功!")
else:
    print(f"[FAIL] 退选失败: {response.text}")

# 验证
print("\n[3] 验证...")
my_selections = requests.get(
    "http://localhost:8000/api/course-selection/my-courses",
    headers=headers
)

if my_selections.status_code == 200:
    selections = my_selections.json()
    found = any(sel['id'] == selection_id for sel in selections)
    if not found:
        print(f"[OK] 课程已成功退选")
    else:
        print(f"[FAIL] 课程仍在列表中")

# 清理
db.query(CourseSelection).filter(CourseSelection.student_id == student.id).delete()
db.commit()

db.close()
print("\n测试完成!")
