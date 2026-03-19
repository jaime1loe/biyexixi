"""课程管理相关API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models import Course, User, CourseSelection
from app.schemas import CourseManagementRequest, CourseWithSelectionStatus
from app.dependencies import get_current_user
from app.routers.activities import log_activity

router = APIRouter(prefix="/course-management", tags=["课程管理"])


@router.post("", summary="开设课程")
async def create_course(
    course: CourseManagementRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员开设新课程"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以开设课程")

    # 检查课程代码是否已存在
    existing = db.query(Course).filter(Course.course_code == course.course_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"课程代码 {course.course_code} 已存在")

    # 验证教师是否存在
    teacher = db.query(User).filter(User.id == course.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="指定的教师不存在")

    if teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="指定的用户不是教师角色")

    # 创建课程
    db_course = Course(
        course_code=course.course_code,
        course_name=course.course_name,
        teacher_id=course.teacher_id,
        teacher_name=teacher.real_name or teacher.username,
        department=course.department,
        credits=course.credits,
        hours=course.hours,
        course_type=course.course_type
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    # 记录活动日志
    log_activity(
        db,
        user_id=current_user.id,
        action_type="开设课程",
        target_type="course",
        target_id=db_course.id,
        target_name=db_course.course_name,
        details=f"为教师 {teacher.real_name or teacher.username} 开设课程：{db_course.course_name}（{db_course.course_code}）"
    )

    return {
        "id": db_course.id,
        "course_code": db_course.course_code,
        "course_name": db_course.course_name,
        "teacher_id": db_course.teacher_id,
        "teacher_name": db_course.teacher_name,
        "department": db_course.department,
        "credits": db_course.credits,
        "hours": db_course.hours,
        "course_type": db_course.course_type
    }


@router.get("", summary="查询所有课程")
async def get_all_courses(
    semester: Optional[str] = Query(None, description="学期"),
    course_type: Optional[str] = Query(None, description="课程类型"),
    department: Optional[str] = Query(None, description="院系"),
    teacher_id: Optional[int] = Query(None, description="教师ID"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员查询所有课程（教师只能查看自己的）"""
    query = db.query(Course).options(joinedload(Course.teacher))

    # 教师只能查看自己的课程
    if current_user.role == "teacher":
        query = query.filter(Course.teacher_id == current_user.id)

    # 筛选条件
    filters = []
    if course_type:
        filters.append(Course.course_type == course_type)
    if department:
        filters.append(Course.department == department)
    if teacher_id:
        filters.append(Course.teacher_id == teacher_id)
    if search:
        filters.append(Course.course_name.like(f"%{search}%") | Course.course_code.like(f"%{search}%"))

    if filters:
        from sqlalchemy import and_
        query = query.filter(and_(*filters))

    courses = query.order_by(Course.created_at.desc()).offset(skip).limit(limit).all()

    total = query.count()

    # 查询每门课程的选课人数
    result = []
    for course in courses:
        selection_count = 0
        if semester:
            selection_count = db.query(CourseSelection).filter(
                CourseSelection.course_id == course.id,
                CourseSelection.semester == semester,
                CourseSelection.status == "selected"
            ).count()

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
            "selection_count": selection_count,
            "created_at": course.created_at
        })

    return {
        "total": total,
        "courses": result
    }


@router.get("/{course_id}", summary="查询课程详情")
async def get_course_detail(
    course_id: int,
    semester: Optional[str] = Query("2024-2025-2", description="学期"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """查询课程详细信息"""
    course = db.query(Course).options(joinedload(Course.teacher)).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 教师只能查看自己的课程
    if current_user.role == "teacher" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限查看该课程")

    # 查询选课人数
    selection_count = db.query(CourseSelection).filter(
        CourseSelection.course_id == course.id,
        CourseSelection.semester == semester,
        CourseSelection.status == "selected"
    ).count()

    return {
        "id": course.id,
        "course_code": course.course_code,
        "course_name": course.course_name,
        "teacher_id": course.teacher_id,
        "teacher_name": course.teacher.real_name if course.teacher else course.teacher_name,
        "department": course.department,
        "credits": course.credits,
        "hours": course.hours,
        "course_type": course.course_type,
        "selection_count": selection_count,
        "created_at": course.created_at,
        "updated_at": course.updated_at
    }


@router.put("/{course_id}", summary="更新课程信息")
async def update_course(
    course_id: int,
    course: CourseManagementRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员或教师更新课程信息"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="权限不足")

    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 教师只能更新自己的课程
    if current_user.role == "teacher" and db_course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限修改该课程")

    # 如果修改了教师，验证教师是否存在
    if course.teacher_id != db_course.teacher_id:
        teacher = db.query(User).filter(User.id == course.teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="指定的教师不存在")
        if teacher.role != "teacher":
            raise HTTPException(status_code=400, detail="指定的用户不是教师角色")
        db_course.teacher_id = course.teacher_id
        db_course.teacher_name = teacher.real_name or teacher.username

    # 如果修改了课程代码，检查是否冲突
    if course.course_code != db_course.course_code:
        existing = db.query(Course).filter(
            Course.course_code == course.course_code,
            Course.id != course_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"课程代码 {course.course_code} 已存在")
        db_course.course_code = course.course_code

    # 更新字段
    db_course.course_name = course.course_name
    db_course.department = course.department
    db_course.credits = course.credits
    db_course.hours = course.hours
    db_course.course_type = course.course_type
    db_course.updated_at = datetime.now()

    db.commit()
    db.refresh(db_course)

    # 记录活动日志
    log_activity(
        db,
        user_id=current_user.id,
        action_type="更新课程",
        target_type="course",
        target_id=db_course.id,
        target_name=db_course.course_name,
        details=f"更新课程信息：{db_course.course_name}（{db_course.course_code}）"
    )

    return {
        "id": db_course.id,
        "course_code": db_course.course_code,
        "course_name": db_course.course_name,
        "teacher_id": db_course.teacher_id,
        "teacher_name": db_course.teacher_name,
        "department": db_course.department,
        "credits": db_course.credits,
        "hours": db_course.hours,
        "course_type": db_course.course_type,
        "updated_at": db_course.updated_at
    }


@router.delete("/{course_id}", summary="删除课程")
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员删除课程"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以删除课程")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 检查是否有选课记录
    selection_count = db.query(CourseSelection).filter(
        CourseSelection.course_id == course_id
    ).count()

    if selection_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"该课程有 {selection_count} 名学生已选课，无法删除"
        )

    # 记录活动日志
    log_activity(
        db,
        user_id=current_user.id,
        action_type="删除课程",
        target_type="course",
        target_id=course.id,
        target_name=course.course_name,
        details=f"删除课程：{course.course_name}（{course.course_code}）"
    )

    db.delete(course)
    db.commit()

    return {"message": "课程删除成功"}


@router.get("/teachers/list", summary="获取教师列表")
async def get_teachers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取所有教师列表（用于开设课程时选择）"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="权限不足")

    teachers = db.query(User).filter(User.role == "teacher").all()

    result = []
    for teacher in teachers:
        result.append({
            "id": teacher.id,
            "username": teacher.username,
            "real_name": teacher.real_name,
            "department": teacher.department
        })

    return result
