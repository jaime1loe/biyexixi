"""测试选课API"""
from app.database import SessionLocal
from app.models import Course, CourseSelection, User

db = SessionLocal()

# 检查课程数据
print("=== 课程数据 ===")
courses = db.query(Course).limit(5).all()
for course in courses:
    print(f"ID: {course.id}, 名称: {course.course_name}, 代码: {course.course_code}, 教师: {course.teacher_name}, 容量: {course.capacity}")

# 检查学生数据
print("\n=== 学生数据 ===")
students = db.query(User).filter(User.role == "student").limit(3).all()
for student in students:
    print(f"ID: {student.id}, 用户名: {student.username}, 姓名: {student.real_name}")

# 检查选课数据
print("\n=== 选课数据 ===")
selections = db.query(CourseSelection).limit(5).all()
for sel in selections:
    print(f"ID: {sel.id}, 学生ID: {sel.student_id}, 课程ID: {sel.course_id}, 学期: {sel.semester}, 状态: {sel.status}")

db.close()
print("\n数据检查完成！")
