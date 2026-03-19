"""测试选课功能完整流程"""
import requests
from app.database import SessionLocal
from app.models import User, Course, CourseSelection
from app.utils import create_access_token

print("=" * 60)
print("测试选课功能完整流程")
print("=" * 60)

# 初始化数据库连接
db = SessionLocal()

# 步骤1: 准备测试数据
print("\n[步骤1] 准备测试数据...")
print("-" * 60)

# 获取一个学生
student = db.query(User).filter(User.role == "student").first()
if not student:
    print("错误: 没有找到学生用户")
    db.close()
    exit(1)

print(f"学生用户: {student.username} (ID: {student.id})")

# 创建token
token = create_access_token(data={"sub": str(student.id)})
headers = {"Authorization": f"Bearer {token}"}
print(f"Token: {token[:30]}...")

# 步骤2: 查询可选课程
print("\n[步骤2] 查询可选课程...")
print("-" * 60)

try:
    response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )

    if response.status_code == 200:
        available_courses = response.json()
        print(f"[OK] 成功获取 {len(available_courses)} 门可选课程")

        if available_courses:
            first_course = available_courses[0]
            print(f"\n第一门课程信息:")
            print(f"  课程名称: {first_course['course_name']}")
            print(f"  课程代码: {first_course['course_code']}")
            print(f"  授课教师: {first_course['teacher_name']}")
            print(f"  容量: {first_course['capacity']}")
            print(f"  已选人数: {first_course['selected_count']}")
            print(f"  剩余名额: {first_course['remaining_count']}")
            print(f"  是否已选: {first_course['is_selected']}")

            test_course_id = first_course['id']
        else:
            print("没有可选课程")
            db.close()
            exit(0)
    else:
        print(f"[FAIL] 查询失败: {response.text}")
        db.close()
        exit(1)
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")
    db.close()
    exit(1)

# 步骤3: 选课
print(f"\n[步骤3] 选择课程 (ID: {test_course_id})...")
print("-" * 60)

try:
    select_data = {
        "course_id": test_course_id,
        "semester": "2024-2025-2"
    }

    response = requests.post(
        "http://localhost:8000/api/course-selection/select",
        headers=headers,
        json=select_data
    )

    if response.status_code == 200:
        selection = response.json()
        print(f"[OK] 选课成功!")
        print(f"  选课ID: {selection['id']}")
        print(f"  课程名称: {selection['course_name']}")
        print(f"  状态: {selection['status']}")
        selection_id = selection['id']
    else:
        print(f"[FAIL] 选课失败: {response.text}")
        db.close()
        exit(1)
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")
    db.close()
    exit(1)

# 步骤4: 查询我的选课
print("\n[步骤4] 查询我的选课...")
print("-" * 60)

try:
    response = requests.get(
        "http://localhost:8000/api/course-selection/my-courses",
        headers=headers
    )

    if response.status_code == 200:
        my_selections = response.json()
        print(f"[OK] 成功获取 {len(my_selections)} 门已选课程")

        if my_selections:
            for sel in my_selections:
                print(f"\n  课程: {sel['course_name']}")
                print(f"    代码: {sel['course_code']}")
                print(f"    状态: {sel['status']}")
    else:
        print(f"[FAIL] 查询失败: {response.text}")
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")

# 步骤5: 再次查询可选课程（验证状态更新）
print("\n[步骤5] 再次查询可选课程（验证状态更新）...")
print("-" * 60)

try:
    response = requests.get(
        "http://localhost:8000/api/course-selection/available",
        headers=headers
    )

    if response.status_code == 200:
        updated_courses = response.json()

        # 找到刚刚选择的课程
        selected_course = None
        for course in updated_courses:
            if course['id'] == test_course_id:
                selected_course = course
                break

        if selected_course:
            print(f"[OK] 课程状态已更新:")
            print(f"  课程名称: {selected_course['course_name']}")
            print(f"  已选人数: {selected_course['selected_count']}")
            print(f"  剩余名额: {selected_course['remaining_count']}")
            print(f"  是否已选: {selected_course['is_selected']}")
    else:
        print(f"[FAIL] 查询失败: {response.text}")
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")

# 步骤6: 测试重复选课（应该失败）
print(f"\n[步骤6] 测试重复选课（应该被拒绝）...")
print("-" * 60)

try:
    select_data = {
        "course_id": test_course_id,
        "semester": "2024-2025-2"
    }

    response = requests.post(
        "http://localhost:8000/api/course-selection/select",
        headers=headers,
        json=select_data
    )

    if response.status_code == 400:
        print(f"[OK] 重复选课被正确拒绝")
        print(f"  错误信息: {response.json()['detail']}")
    else:
        print(f"[FAIL] 重复选课应该被拒绝，但返回了 {response.status_code}")
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")

# 步骤7: 退选课程
print(f"\n[步骤7] 退选课程 (ID: {selection_id})...")
print("-" * 60)

try:
    response = requests.delete(
        f"http://localhost:8000/api/course-selection/{selection_id}",
        headers=headers
    )

    if response.status_code == 200:
        print(f"[OK] 退选成功")
    else:
        print(f"[FAIL] 退选失败: {response.text}")
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")

# 步骤8: 再次查询我的选课（验证退选成功）
print("\n[步骤8] 再次查询我的选课（验证退选成功）...")
print("-" * 60)

try:
    response = requests.get(
        "http://localhost:8000/api/course-selection/my-courses",
        headers=headers
    )

    if response.status_code == 200:
        my_selections = response.json()
        print(f"[OK] 当前选课数量: {len(my_selections)}")

        # 验证退选的课程不在列表中
        found = any(sel['id'] == selection_id for sel in my_selections)
        if not found:
            print(f"[OK] 课程已成功退选，不在列表中")
        else:
            print(f"[FAIL] 退选失败，课程仍在列表中")
    else:
        print(f"[FAIL] 查询失败: {response.text}")
except Exception as e:
    print(f"[ERROR] 请求异常: {e}")

# 步骤9: 测试教师功能
print("\n[步骤9] 测试教师功能...")
print("-" * 60)

# 获取一个教师
teacher = db.query(User).filter(User.role == "teacher").first()
if teacher:
    teacher_token = create_access_token(data={"sub": str(teacher.id)})
    teacher_headers = {"Authorization": f"Bearer {teacher_token}"}

    print(f"教师用户: {teacher.username} (ID: {teacher.id})")

    # 查询教师的课程及选课情况
    try:
        response = requests.get(
            "http://localhost:8000/api/course-selection/teacher/my-courses",
            headers=teacher_headers
        )

        if response.status_code == 200:
            teacher_courses = response.json()
            print(f"[OK] 成功获取教师的 {len(teacher_courses)} 门课程")

            if teacher_courses:
                for course in teacher_courses:
                    print(f"\n  课程: {course['course_name']}")
                    print(f"    选课人数: {course['selection_count']}")
                    print(f"    学期: {course['semester']}")
        else:
            print(f"[FAIL] 查询失败: {response.text}")
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
else:
    print("没有找到教师用户")

# 清理数据库中的测试选课记录
print("\n[清理] 删除测试选课记录...")
db.query(CourseSelection).filter(CourseSelection.student_id == student.id).delete()
db.commit()
print("[OK] 测试数据已清理")

db.close()

print("\n" + "=" * 60)
print("[SUCCESS] 选课功能完整流程测试完成!")
print("=" * 60)
