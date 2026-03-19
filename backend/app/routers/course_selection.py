"""课程选课相关API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models import CourseSelection, Course, User, Grade
from app.schemas import (
    CourseSelectionCreate,
    CourseSelectionResponse,
    CourseWithSelectionStatus,
    CourseManagementRequest
)
from app.dependencies import get_current_user
from app.routers.activities import log_activity

router = APIRouter(prefix="/course-selection", tags=["课程选课"])


@router.get("/available", response_model=List[CourseWithSelectionStatus], summary="查询可选课程")
async def get_available_courses(
    semester: str = Query("2024-2025-2", description="学期"),
    course_type: Optional[str] = Query(None, description="课程类型：必修/选修/实践"),
    department: Optional[str] = Query(None, description="院系筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生查询可选课程列表"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="只有学生可以选课")

    # 查询所有课程
    query = db.query(Course).options(joinedload(Course.teacher))

    # 筛选条件
    filters = []
    if course_type:
        filters.append(Course.course_type == course_type)
    if department:
        filters.append(Course.department == department)
    if search:
        filters.append(or_(
            Course.course_name.like(f"%{search}%"),
            Course.course_code.like(f"%{search}%")
        ))

    if filters:
        query = query.filter(and_(*filters))

    courses = query.all()

    # 查询学生已选的课程
    my_selections = db.query(CourseSelection).filter(
        CourseSelection.student_id == current_user.id,
        CourseSelection.semester == semester
    ).all()

    selected_course_ids = {sel.course_id: sel for sel in my_selections}

    # 查询每门课程的选课人数
    course_selections_count = db.query(
        CourseSelection.course_id,
        func.count(CourseSelection.id).label('count')
    ).filter(
        CourseSelection.semester == semester,
        CourseSelection.status == "selected"
    ).group_by(CourseSelection.course_id).all()

    selection_count_map = {item[0]: item[1] for item in course_selections_count}

    # 构建响应
    result = []
    for course in courses:
        is_selected = course.id in selected_course_ids
        selection_status = selected_course_ids[course.id].status if is_selected else None
        selected_count = selection_count_map.get(course.id, 0)
        capacity = course.capacity or 100
        remaining_count = max(0, capacity - selected_count)

        result.append({
            "id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "teacher_id": course.teacher_id,
            "teacher_name": course.teacher.real_name if course.teacher else course.teacher_name,
            "department": course.department,
            "credits": course.credits,
            "hours": course.hours,
            "course_type": course.course_type,
            "capacity": capacity,
            "selected_count": selected_count,
            "remaining_count": remaining_count,
            "is_selected": is_selected,
            "selection_status": selection_status
        })

    return result


@router.get("/my-courses", response_model=List[CourseSelectionResponse], summary="我的选课")
async def get_my_selections(
    semester: str = Query("2024-2025-2", description="学期"),
    status: Optional[str] = Query(None, description="状态筛选：selected/dropped/completed"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生查询自己的选课记录"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="只有学生可以查看选课")

    query = db.query(CourseSelection).options(joinedload(CourseSelection.course)).filter(
        CourseSelection.student_id == current_user.id,
        CourseSelection.semester == semester
    )

    if status:
        query = query.filter(CourseSelection.status == status)

    selections = query.order_by(CourseSelection.selected_at.desc()).all()

    result = []
    for selection in selections:
        course = selection.course
        result.append({
            "id": selection.id,
            "student_id": selection.student_id,
            "course_id": selection.course_id,
            "course_code": course.course_code if course else "",
            "course_name": course.course_name if course else "",
            "teacher_id": course.teacher_id if course else None,
            "teacher_name": course.teacher_name if course else "",
            "semester": selection.semester,
            "status": selection.status,
            "selected_at": selection.selected_at,
            "dropped_at": selection.dropped_at,
            "course_type": course.course_type if course else None,
            "credits": course.credits if course else None,
            "hours": course.hours if course else None,
            "department": course.department if course else None
        })

    return result


@router.post("/select", response_model=CourseSelectionResponse, summary="选课")
async def select_course(
    selection: CourseSelectionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生选择课程"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="只有学生可以选课")

    # 验证课程是否存在
    course = db.query(Course).filter(Course.id == selection.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 检查是否已经选过该课程（同同学期）
    existing = db.query(CourseSelection).filter(
        CourseSelection.student_id == current_user.id,
        CourseSelection.course_id == selection.course_id,
        CourseSelection.semester == selection.semester
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="您已选择过该课程，不能重复选课")

    # 创建选课记录
    db_selection = CourseSelection(
        student_id=current_user.id,
        course_id=selection.course_id,
        semester=selection.semester,
        status="selected"
    )

    db.add(db_selection)
    db.commit()
    db.refresh(db_selection)

    # 记录活动日志
    log_activity(
        db,
        user_id=current_user.id,
        action_type="选课",
        target_type="course",
        target_id=course.id,
        target_name=course.course_name,
        details=f"选择了课程：{course.course_name}（{course.course_code}）"
    )

    # 构建响应
    result = {
        "id": db_selection.id,
        "student_id": db_selection.student_id,
        "course_id": db_selection.course_id,
        "course_code": course.course_code,
        "course_name": course.course_name,
        "teacher_id": course.teacher_id,
        "teacher_name": course.teacher_name,
        "semester": db_selection.semester,
        "status": db_selection.status,
        "selected_at": db_selection.selected_at,
        "dropped_at": None,
        "course_type": course.course_type,
        "credits": course.credits,
        "hours": course.hours,
        "department": course.department
    }

    return result


@router.delete("/{selection_id}", summary="退选")
async def drop_course(
    selection_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生退选课程"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="只有学生可以退选")

    selection = db.query(CourseSelection).filter(
        CourseSelection.id == selection_id,
        CourseSelection.student_id == current_user.id
    ).first()

    if not selection:
        raise HTTPException(status_code=404, detail="选课记录不存在")

    course = db.query(Course).filter(Course.id == selection.course_id).first()

    # 检查是否已有成绩记录
    grade = db.query(Grade).filter(
        Grade.student_id == current_user.id,
        Grade.course_id == selection.course_id
    ).first()

    if grade:
        raise HTTPException(status_code=400, detail="该课程已有成绩记录，无法退选")

    # 更新状态
    selection.status = "dropped"
    selection.dropped_at = datetime.now()
    db.commit()

    # 记录活动日志
    if course:
        log_activity(
            db,
            user_id=current_user.id,
            action_type="退选",
            target_type="course",
            target_id=course.id,
            target_name=course.course_name,
            details=f"退选课程：{course.course_name}（{course.course_code}）"
        )

    return {"message": "退选成功"}


@router.get("/teacher/{course_id}/students", summary="教师查看课程选课学生")
async def get_course_selection_students(
    course_id: int,
    semester: str = Query("2024-2025-2", description="学期"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """教师查看某课程的选课学生列表"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以查看")

    # 验证课程是否属于该教师
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限查看该课程的选课信息")

    # 查询选课学生
    selections = db.query(CourseSelection).options(joinedload(CourseSelection.student)).filter(
        CourseSelection.course_id == course_id,
        CourseSelection.semester == semester,
        CourseSelection.status == "selected"
    ).all()

    result = []
    for selection in selections:
        student = selection.student
        result.append({
            "student_id": student.id,
            "student_name": student.real_name or student.username,
            "student_number": student.student_id,
            "department": student.department,
            "major": student.major,
            "class_name": student.class_name,
            "selected_at": selection.selected_at,
            "selection_id": selection.id
        })

    return result


@router.get("/teacher/my-courses", summary="教师查看自己的课程及选课情况")
async def get_teacher_course_selections(
    semester: str = Query("2024-2025-2", description="学期"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """教师查看自己的课程及选课情况"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以查看")

    # 查询教师的课程（Course表本身有semester字段吗？如果没有则查询所有课程，只通过选课记录筛选）
    from app.models import CourseSelection as CS

    # 先查询该学期教师有选课记录的课程
    course_ids_with_selections = db.query(CS.course_id).filter(
        CS.semester == semester,
        CS.status == "selected"
    ).distinct().all()

    course_ids_with_selections = [cid[0] for cid in course_ids_with_selections]

    # 查询教师的所有课程
    courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()

    result = []
    for course in courses:
        # 查询该课程在该学期的选课人数
        selection_count = db.query(CourseSelection).filter(
            CourseSelection.course_id == course.id,
            CourseSelection.semester == semester,
            CourseSelection.status == "selected"
        ).count()

        # 只返回有选课记录的课程，或者返回所有课程但显示选课人数为0
        result.append({
            "course_id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "course_type": course.course_type,
            "credits": course.credits,
            "hours": course.hours,
            "department": course.department,
            "selection_count": selection_count,
            "semester": semester
        })

    return result
