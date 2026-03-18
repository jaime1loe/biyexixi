#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查成绩数据"""
import sys
sys.path.insert(0, '..')

from app.database import SessionLocal, engine
from app.models import User, Course, Grade

db = SessionLocal()

print("=== 检查用户数据 ===")
users = db.query(User).filter(User.role == 'student').all()
for user in users[:5]:
    print(f"用户ID: {user.id}, 用户名: {user.username}, 真实姓名: {user.real_name}")

print("\n=== 检查课程数据 ===")
courses = db.query(Course).limit(5).all()
for course in courses:
    print(f"课程ID: {course.id}, 课程代码: {course.course_code}, 课程名称: {course.course_name}, 教师ID: {course.teacher_id}")

print("\n=== 检查成绩数据 ===")
grades = db.query(Grade).limit(5).all()
for grade in grades:
    print(f"成绩ID: {grade.id}, 学生ID: {grade.student_id}, 课程ID: {grade.course_id}, 学期: {grade.semester}, 成绩: {grade.score}")

print("\n=== 检查特定学生的成绩 ===")
test_user_id = db.query(User.id).filter(User.username == 'testuser').first()
if test_user_id:
    student_grades = db.query(Grade).filter(Grade.student_id == test_user_id).all()
    print(f"testuser (ID: {test_user_id}) 的成绩数量: {len(student_grades)}")
    for grade in student_grades:
        print(f"  课程ID: {grade.course_id}, 学期: {grade.semester}, 成绩: {grade.score}")
else:
    print("未找到testuser")

db.close()
