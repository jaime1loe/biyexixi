#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为教师分配课程"""
import sys
sys.path.insert(0, 'd:/毕业设计')

from app.database import SessionLocal
from app.models import User, Course, Schedule
import random

def assign_teachers_to_courses():
    """为课程分配教师"""
    db = SessionLocal()

    try:
        print("=== 为课程分配教师 ===\n")

        # 获取教师和课程
        teachers = db.query(User).filter(User.role == 'teacher').all()
        courses = db.query(Course).all()

        print(f"找到 {len(teachers)} 个教师")
        print(f"找到 {len(courses)} 门课程\n")

        if not teachers:
            print("没有教师用户，无法分配")
            return

        # 为没有教师的课程分配教师
        count = 0
        for course in courses:
            if course.teacher_id is None:
                # 随机分配一个教师
                teacher = random.choice(teachers)
                course.teacher_id = teacher.id
                course.teacher_name = teacher.real_name or teacher.username
                count += 1
                print(f"分配: {teacher.real_name or teacher.username} -> {course.course_code} {course.course_name}")

        if count == 0:
            print("所有课程都已分配教师")
        else:
            db.commit()
            print(f"\n[OK] 成功为 {count} 门课程分配教师")

        # 验证排课情况
        print("\n验证排课情况:")
        for teacher in teachers:
            teacher_courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()
            if teacher_courses:
                print(f"\n教师: {teacher.real_name or teacher.username}")
                for course in teacher_courses[:5]:  # 只显示前5门
                    schedules = db.query(Schedule).filter(Schedule.course_id == course.id).all()
                    if schedules:
                        semesters = list(set(s.semester for s in schedules))
                        print(f"  - {course.course_name} (学期: {', '.join(semesters)})")
                    else:
                        print(f"  - {course.course_name} (未排课)")

        print("\n=== 完成 ===")

    except Exception as e:
        print(f"错误: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    assign_teachers_to_courses()
