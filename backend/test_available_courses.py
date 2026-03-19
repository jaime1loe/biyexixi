"""测试可选课程API"""
from app.database import SessionLocal
from app.models import CourseSelection, Course, User
from sqlalchemy import func

db = SessionLocal()

try:
    # 获取一个学生用户
    student = db.query(User).filter(User.role == "student").first()
    if not student:
        print("没有找到学生用户")
    else:
        print(f"使用学生: {student.username} (ID: {student.id})")
        semester = "2024-2025-2"

        # 模拟API查询逻辑
        print("\n=== 查询所有课程 ===")
        courses = db.query(Course).all()
        print(f"找到 {len(courses)} 门课程")

        print("\n=== 查询学生已选课程 ===")
        my_selections = db.query(CourseSelection).filter(
            CourseSelection.student_id == student.id,
            CourseSelection.semester == semester
        ).all()
        print(f"学生已选 {len(my_selections)} 门课程")

        print("\n=== 查询每门课程的选课人数 ===")
        course_selections_count = db.query(
            CourseSelection.course_id,
            func.count(CourseSelection.id).label('count')
        ).filter(
            CourseSelection.semester == semester,
            CourseSelection.status == "selected"
        ).group_by(CourseSelection.course_id).all()

        selection_count_map = {item[0]: item[1] for item in course_selections_count}
        print(f"有选课记录的课程: {len(selection_count_map)}")
        for course_id, count in selection_count_map.items():
            print(f"  课程ID {course_id}: {count} 人")

        print("\n=== 构建响应数据 ===")
        result = []
        for course in courses[:3]:  # 只测试前3门
            print(f"处理课程: {course.course_name} (ID: {course.id})")
            selected_count = selection_count_map.get(course.id, 0)
            capacity = getattr(course, 'capacity', 100)
            print(f"  容量: {capacity}, 已选: {selected_count}")
            remaining_count = max(0, capacity - selected_count)
            print(f"  剩余: {remaining_count}")

        print("\n测试完成，未发现错误！")

except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
