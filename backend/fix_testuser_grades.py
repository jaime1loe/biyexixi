#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为testuser创建测试成绩"""
import sys
sys.path.insert(0, '..')

from app.database import SessionLocal
from app.models import User, Course, Grade
from datetime import datetime

db = SessionLocal()

# 获取testuser
testuser = db.query(User).filter(User.username == 'testuser').first()
if not testuser:
    print("未找到testuser")
    db.close()
    sys.exit(1)

print(f"testuser ID: {testuser.id}, 姓名: {testuser.real_name}")

# 检查现有成绩
existing_grades = db.query(Grade).filter(Grade.student_id == testuser.id).all()
print(f"现有成绩数量: {len(existing_grades)}")

# 如果没有成绩，创建一些
if len(existing_grades) == 0:
    # 获取现有课程
    courses = db.query(Course).limit(5).all()
    print(f"可用课程数: {len(courses)}")

    if len(courses) == 0:
        # 创建测试课程
        print("没有课程，创建测试课程...")
        course = Course(
            course_code='CS001',
            course_name='计算机导论',
            teacher_id=1,
            teacher_name='张老师',
            department='计算机学院',
            credits=3.0,
            hours=48,
            course_type='必修'
        )
        db.add(course)
        db.flush()
        courses = [course]

    # 为testuser创建成绩
    for course in courses:
        # 检查是否已有该课程的成绩
        existing = db.query(Grade).filter(
            Grade.student_id == testuser.id,
            Grade.course_id == course.id
        ).first()

        if existing:
            print(f"  已有成绩: {course.course_name}")
            continue

        grade = Grade(
            student_id=testuser.id,
            course_id=course.id,
            semester='2024-2025-1',
            score=85.0,
            grade_point=3.7,
            grade_level='B',
            is_makeup=False,
            created_at=datetime.now()
        )
        db.add(grade)
        print(f"  创建成绩: {course.course_name} - {grade.score}分")

    db.commit()
    print("\n成绩数据创建完成")
else:
    print("\ntestuser已有成绩数据")

# 验证
all_grades = db.query(Grade).filter(Grade.student_id == testuser.id).all()
print(f"\n总成绩数: {len(all_grades)}")
for grade in all_grades:
    course = db.query(Course).filter(Course.id == grade.course_id).first()
    if course:
        print(f"  {course.course_name} ({course.course_code}): {grade.score}分 - {grade.semester}")

db.close()
