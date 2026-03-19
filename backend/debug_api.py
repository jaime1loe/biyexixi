"""调试API端点"""
import sys
import traceback

# 直接导入并测试
try:
    from app.database import SessionLocal
    from app.models import Course, CourseSelection, User
    from app.schemas import CourseWithSelectionStatus
    from sqlalchemy import func

    print("=== 导入成功 ===")

    db = SessionLocal()

    # 获取一个学生
    student = db.query(User).filter(User.role == "student").first()
    if not student:
        print("没有找到学生用户")
        sys.exit(1)

    print(f"找到学生: {student.username} (ID: {student.id})")

    # 测试查询课程
    semester = "2024-2025-2"
    courses = db.query(Course).all()
    print(f"查询到 {len(courses)} 门课程")

    # 测试查询选课人数
    course_selections_count = db.query(
        CourseSelection.course_id,
        func.count(CourseSelection.id).label('count')
    ).filter(
        CourseSelection.semester == semester,
        CourseSelection.status == "selected"
    ).group_by(CourseSelection.course_id).all()

    selection_count_map = {item[0]: item[1] for item in course_selections_count}
    print(f"选课人数查询成功，覆盖 {len(selection_count_map)} 门课程")

    # 测试构建响应
    for course in courses[:1]:
        selected_count = selection_count_map.get(course.id, 0)
        capacity = getattr(course, 'capacity', 100)
        remaining_count = max(0, capacity - selected_count)

        result = {
            "id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "teacher_id": course.teacher_id,
            "teacher_name": course.teacher_name,
            "department": course.department,
            "credits": course.credits,
            "hours": course.hours,
            "course_type": course.course_type,
            "capacity": capacity,
            "selected_count": selected_count,
            "remaining_count": remaining_count,
            "is_selected": False,
            "selection_status": None
        }

        print(f"响应构建成功: {result['course_name']}")

    db.close()
    print("\n所有测试通过！")

except Exception as e:
    print(f"\n发生错误: {e}")
    traceback.print_exc()
