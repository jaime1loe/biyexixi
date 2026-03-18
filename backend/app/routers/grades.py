#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""成绩管理API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from sqlalchemy import func

from app.database import get_db
from app.models import User, Course, Grade, Schedule
from app.schemas import (
    GradeCreate,
    GradeUpdate,
    GradeResponse,
    GradeUpload,
    StudentGradeResponse
)
from app.dependencies import get_current_user

router = APIRouter(tags=["成绩管理"])


def calculate_grade_point(score: float) -> float:
    """计算绩点"""
    if score >= 90:
        return 4.0
    elif score >= 85:
        return 3.7
    elif score >= 82:
        return 3.3
    elif score >= 78:
        return 3.0
    elif score >= 75:
        return 2.7
    elif score >= 72:
        return 2.3
    elif score >= 68:
        return 2.0
    elif score >= 66:
        return 1.7
    elif score >= 64:
        return 1.3
    elif score >= 60:
        return 1.0
    else:
        return 0.0


def calculate_grade_level(score: float) -> str:
    """计算等级"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


@router.get("/student/my", summary="学生查询我的成绩")
async def get_my_grades(
    semester: Optional[str] = Query(None, description="学期过滤"),
    course_name: Optional[str] = Query(None, description="课程名称过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """学生查询自己的成绩列表"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="只有学生可以查询自己的成绩")

    query = db.query(Grade).filter(Grade.student_id == current_user.id)

    if semester:
        query = query.filter(Grade.semester == semester)

    grades = query.options(joinedload(Grade.course)).order_by(Grade.semester.desc()).all()

    result = []
    for grade in grades:
        # 检查课程是否存在
        if not grade.course:
            print(f"警告: 成绩ID {grade.id} 没有关联的课程，课程ID: {grade.course_id}")
            continue

        # 如果指定了课程名称，进行过滤
        if course_name and course_name.lower() not in grade.course.course_name.lower():
            continue

        # 直接构建字典
        result.append({
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "semester": grade.semester,
            "course_code": grade.course.course_code,
            "course_name": grade.course.course_name,
            "credits": grade.course.credits or 0,
            "score": grade.score,
            "grade_point": grade.grade_point,
            "grade_level": grade.grade_level,
            "is_makeup": grade.is_makeup,
            "gpa": None  # 稍后计算
        })

    print(f"返回 {len(result)} 条成绩记录")

    # 计算GPA
    if result:
        total_credits = sum(g["credits"] for g in result)
        total_grade_points = sum(g["credits"] * g["grade_point"] for g in result)
        gpa = total_grade_points / total_credits if total_credits > 0 else 0

        for item in result:
            item["gpa"] = round(gpa, 2)

    return result


@router.get("/teacher/courses", response_model=List[dict], summary="教师获取所授课程列表")
async def get_teacher_courses(
    semester: Optional[str] = Query(None, description="学期过滤"),
    course_name: Optional[str] = Query(None, description="课程名称过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """教师获取自己所授的课程列表"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="只有教师可以查看授课列表")

    # 获取教师的所有课程ID
    query = db.query(Course).filter(Course.teacher_id == current_user.id)

    if semester:
        # 如果指定了学期，通过Schedule筛选有排课的课程
        subquery = db.query(Schedule.course_id).filter(
            Schedule.semester == semester
        ).distinct()
        query = query.filter(Course.id.in_(subquery))

    courses = query.all()

    # 返回结果
    result = []
    for course in courses:
        # 获取该课程的学期信息
        if semester:
            course_semester = semester
        else:
            # 如果没有指定学期，获取该课程最新的学期
            latest_schedule = db.query(Schedule).filter(
                Schedule.course_id == course.id
            ).order_by(Schedule.created_at.desc()).first()
            course_semester = latest_schedule.semester if latest_schedule else "未安排"

        # 如果指定了课程名称，进行过滤
        if course_name and course_name.lower() not in course.course_name.lower():
            continue

        result.append({
            "id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "semester": course_semester,
            "credits": course.credits,
            "student_count": db.query(Grade).filter(Grade.course_id == course.id).count()
        })

    return result


@router.get("/teacher/course/{course_id}/students", response_model=List[dict], summary="获取课程学生列表（无成绩或需要录入）")
async def get_course_students(
    course_id: int,
    semester: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取某门课程的学生列表，包含已录入的成绩"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="只有教师可以查看学生列表")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    if course.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="您不是该课程的授课教师")

    # 获取所有已录入成绩的学生
    grades = db.query(Grade).filter(
        Grade.course_id == course_id,
        Grade.semester == semester
    ).options(joinedload(Grade.student)).all()

    result = []
    for grade in grades:
        result.append({
            "student_id": grade.student_id,
            "student_name": grade.student.real_name or grade.student.username,
            "student_number": grade.student.student_id,
            "score": grade.score,
            "grade_level": grade.grade_level,
            "is_makeup": grade.is_makeup,
            "grade_id": grade.id
        })

    return result


@router.post("/teacher/upload", response_model=List[GradeResponse], summary="教师上传学生成绩")
async def upload_grades(
    grade_upload: GradeUpload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """教师批量上传学生成绩"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="只有教师可以上传成绩")

    course = db.query(Course).filter(Course.id == grade_upload.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    if course.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="您不是该课程的授课教师")

    if len(grade_upload.student_ids) != len(grade_upload.scores):
        raise HTTPException(status_code=400, detail="学生数量和成绩数量不匹配")

    results = []
    for i, student_id in enumerate(grade_upload.student_ids):
        # 检查学生是否存在
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            raise HTTPException(status_code=404, detail=f"学生ID {student_id} 不存在或不是学生")

        # 检查是否已有成绩
        existing_grade = db.query(Grade).filter(
            Grade.student_id == student_id,
            Grade.course_id == grade_upload.course_id,
            Grade.semester == grade_upload.semester
        ).first()

        score = grade_upload.scores[i]
        grade_point = calculate_grade_point(score)
        grade_level = calculate_grade_level(score)

        if existing_grade:
            # 更新成绩
            existing_grade.score = score
            existing_grade.grade_point = grade_point
            existing_grade.grade_level = grade_level
            existing_grade.teacher_id = current_user.id
            grade = existing_grade
        else:
            # 创建新成绩
            grade = Grade(
                student_id=student_id,
                course_id=grade_upload.course_id,
                semester=grade_upload.semester,
                score=score,
                grade_point=grade_point,
                grade_level=grade_level,
                teacher_id=current_user.id
            )
            db.add(grade)

        db.flush()
        results.append(grade)

    db.commit()

    # 重新查询以加载关联数据
    return db.query(Grade).filter(
        Grade.id.in_([g.id for g in results])
    ).options(joinedload(Grade.course), joinedload(Grade.student)).all()


@router.put("/teacher/grade/{grade_id}", response_model=GradeResponse, summary="教师修改学生成绩")
async def update_grade(
    grade_id: int,
    grade_update: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """教师修改单个学生成绩"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="只有教师可以修改成绩")

    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="成绩记录不存在")

    course = db.query(Course).filter(Course.id == grade.course_id).first()
    if course.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="您不是该课程的授课教师")

    if grade_update.score is not None:
        grade.score = grade_update.score
        grade.grade_point = calculate_grade_point(grade_update.score)
        grade.grade_level = calculate_grade_level(grade_update.score)

    if grade_update.is_makeup is not None:
        grade.is_makeup = grade_update.is_makeup

    grade.teacher_id = current_user.id
    db.commit()
    db.refresh(grade)

    return grade


@router.delete("/teacher/grade/{grade_id}", summary="教师删除学生成绩")
async def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """教师删除单个学生成绩"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="只有教师可以删除成绩")

    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="成绩记录不存在")

    course = db.query(Course).filter(Course.id == grade.course_id).first()
    if course.teacher_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="您不是该课程的授课教师")

    db.delete(grade)
    db.commit()

    return {"message": "成绩已删除"}


@router.get("/admin/all", response_model=List[GradeResponse], summary="管理员查询所有成绩（需要管理员权限）")
async def get_all_grades(
    semester: Optional[str] = Query(None, description="学期过滤"),
    student_id: Optional[int] = Query(None, description="学生ID过滤"),
    course_id: Optional[int] = Query(None, description="课程ID过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """管理员查询所有成绩列表"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")

    query = db.query(Grade)

    if semester:
        query = query.filter(Grade.semester == semester)
    if student_id:
        query = query.filter(Grade.student_id == student_id)
    if course_id:
        query = query.filter(Grade.course_id == course_id)

    return query.options(joinedload(Grade.course), joinedload(Grade.student), joinedload(Grade.teacher)).all()
