#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建测试课程和成绩数据"""
import sys
sys.path.insert(0, '..')

from app.database import SessionLocal
from app.models import User, Course, Grade
from datetime import datetime

db = SessionLocal()

# 获取学生用户
student = db.query(User).filter(User.username == 'testuser').first()
if not student:
    print("未找到testuser学生，请先注册")
    db.close()
    sys.exit(1)

# 获取教师用户
teacher = db.query(User).filter(User.role == 'teacher').first()
if not teacher:
    print("未找到教师用户")
    db.close()
    sys.exit(1)

print(f"学生: {student.username} (ID: {student.id})")
print(f"教师: {teacher.username} (ID: {teacher.id})")

# 创建测试课程
courses_data = [
    {
        'course_code': 'CS101',
        'course_name': '计算机基础',
        'teacher_id': teacher.id,
        'teacher_name': teacher.real_name or teacher.username,
        'department': '计算机学院',
        'credits': 3.0,
        'hours': 48,
        'course_type': '必修'
    },
    {
        'course_code': 'CS102',
        'course_name': '数据结构',
        'teacher_id': teacher.id,
        'teacher_name': teacher.real_name or teacher.username,
        'department': '计算机学院',
        'credits': 4.0,
        'hours': 64,
        'course_type': '必修'
    },
    {
        'course_code': 'CS103',
        'course_name': '算法设计',
        'teacher_id': teacher.id,
        'teacher_name': teacher.real_name or teacher.username,
        'department': '计算机学院',
        'credits': 3.0,
        'hours': 48,
        'course_type': '必修'
    },
    {
        'course_code': 'CS104',
        'course_name': '数据库原理',
        'teacher_id': teacher.id,
        'teacher_name': teacher.real_name or teacher.username,
        'department': '计算机学院',
        'credits': 3.0,
        'hours': 48,
        'course_type': '必修'
    }
]

print("\n创建测试课程...")
for course_data in courses_data:
    # 检查是否已存在
    existing = db.query(Course).filter(Course.course_code == course_data['course_code']).first()
    if existing:
        print(f"  课程 {course_data['course_code']} 已存在")
        continue

    course = Course(**course_data)
    db.add(course)
    db.flush()  # 获取ID
    print(f"  创建课程: {course.course_name} (ID: {course.id})")

    # 创建成绩
    grade = Grade(
        student_id=student.id,
        course_id=course.id,
        semester='2024-2025-1',
        score=85.0,
        grade_point=3.7,
        grade_level='B',
        is_makeup=False,
        created_at=datetime.now()
    )
    db.add(grade)
    print(f"    创建成绩: {score}分")

db.commit()
print("\n✅ 测试数据创建完成")

# 验证
print("\n=== 验证数据 ===")
all_courses = db.query(Course).all()
print(f"总课程数: {len(all_courses)}")

all_grades = db.query(Grade).filter(Grade.student_id == student.id).all()
print(f"{student.username}的成绩数: {len(all_grades)}")
for grade in all_grades:
    course = db.query(Course).filter(Course.id == grade.course_id).first()
    print(f"  {course.course_name if course else 'Unknown'}: {grade.score}分")

db.close()
