"""课程评价相关API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models import CourseEvaluation, Course, User, Grade
from app.schemas import CourseEvaluationCreate, CourseEvaluationUpdate, CourseEvaluationResponse, CourseEvaluationStats
from app.dependencies import get_current_user

router = APIRouter(prefix="/evaluations", tags=["课程评价"])


@router.post("", response_model=CourseEvaluationResponse, summary="提交课程评价")
async def create_evaluation(
    evaluation: CourseEvaluationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生提交课程评价"""
    # 验证课程是否存在
    course = db.query(Course).filter(Course.id == evaluation.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 验证学生是否已修过该课程
    grade = db.query(Grade).filter(
        Grade.student_id == current_user.id,
        Grade.course_id == evaluation.course_id
    ).first()
    if not grade:
        raise HTTPException(status_code=400, detail="您未修过该课程，无法评价")

    # 检查是否已经评价过
    existing = db.query(CourseEvaluation).filter(
        CourseEvaluation.student_id == current_user.id,
        CourseEvaluation.course_id == evaluation.course_id,
        CourseEvaluation.semester == evaluation.semester
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已评价过该课程")

    # 创建评价
    db_evaluation = CourseEvaluation(
        student_id=current_user.id,
        course_id=evaluation.course_id,
        teacher_id=course.teacher_id,
        semester=evaluation.semester,
        teaching_quality=evaluation.teaching_quality,
        course_content=evaluation.course_content,
        teacher_attitude=evaluation.teacher_attitude,
        difficulty=evaluation.difficulty,
        workload=evaluation.workload,
        overall_rating=evaluation.overall_rating,
        comment=evaluation.comment,
        is_recommended=evaluation.is_recommended
    )

    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)

    # 构建响应数据
    result = build_evaluation_response(db_evaluation, course, current_user)

    return result


@router.get("/my-evaluations", response_model=List[CourseEvaluationResponse], summary="我的评价")
async def get_my_evaluations(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生查询自己的评价记录"""
    query = db.query(CourseEvaluation).filter(
        CourseEvaluation.student_id == current_user.id
    )

    if semester:
        query = query.filter(CourseEvaluation.semester == semester)

    evaluations = query.order_by(CourseEvaluation.created_at.desc()).all()

    results = []
    for eval in evaluations:
        course = db.query(Course).filter(Course.id == eval.course_id).first()
        result = build_evaluation_response(eval, course, current_user)
        results.append(result)

    return results


@router.get("/course/{course_id}", response_model=List[CourseEvaluationResponse], summary="课程评价列表")
async def get_course_evaluations(
    course_id: int,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """查询指定课程的评价（教师可查看）"""
    # 验证课程是否存在
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 验证权限（教师只能查看自己课程的评价）
    if current_user.role == "teacher" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他课程的评价")

    query = db.query(CourseEvaluation).filter(
        CourseEvaluation.course_id == course_id
    )

    if semester:
        query = query.filter(CourseEvaluation.semester == semester)

    evaluations = query.order_by(CourseEvaluation.created_at.desc()).all()

    results = []
    for eval in evaluations:
        student = db.query(User).filter(User.id == eval.student_id).first()
        result = build_evaluation_response(eval, course, student)
        results.append(result)

    return results


@router.get("/teacher/my-courses-stats", response_model=List[CourseEvaluationStats], summary="我的课程评价统计")
async def get_teacher_course_stats(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """教师查询自己课程的评价统计"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="只有教师可以查看")

    # 获取教师的所有课程
    courses_query = db.query(Course).filter(Course.teacher_id == current_user.id)

    results = []
    for course in courses_query.all():
        query = db.query(CourseEvaluation).filter(
            CourseEvaluation.course_id == course.id
        )

        if semester:
            query = query.filter(CourseEvaluation.semester == semester)

        evaluations = query.all()

        if evaluations:
            # 计算平均分
            avg_quality = sum(e.teaching_quality for e in evaluations) / len(evaluations)
            avg_content = sum(e.course_content for e in evaluations) / len(evaluations)
            avg_attitude = sum(e.teacher_attitude for e in evaluations) / len(evaluations)
            avg_difficulty = sum(e.difficulty for e in evaluations) / len(evaluations)
            avg_workload = sum(e.workload for e in evaluations) / len(evaluations)
            avg_overall = sum(e.overall_rating for e in evaluations) / len(evaluations)

            # 计算推荐率
            recommendation_rate = sum(1 for e in evaluations if e.is_recommended == 1) / len(evaluations) * 100

            results.append(CourseEvaluationStats(
                course_id=course.id,
                course_name=course.course_name,
                teacher_name=current_user.real_name or current_user.username,
                semester=semester or "全部",
                total_evaluations=len(evaluations),
                average_ratings={
                    "teaching_quality": round(avg_quality, 2),
                    "course_content": round(avg_content, 2),
                    "teacher_attitude": round(avg_attitude, 2),
                    "difficulty": round(avg_difficulty, 2),
                    "workload": round(avg_workload, 2),
                    "overall_rating": round(avg_overall, 2)
                },
                recommendation_rate=round(recommendation_rate, 2)
            ))

    return results


@router.put("/{evaluation_id}", response_model=CourseEvaluationResponse, summary="修改评价")
async def update_evaluation(
    evaluation_id: int,
    evaluation_update: CourseEvaluationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生修改自己的评价"""
    evaluation = db.query(CourseEvaluation).filter(
        CourseEvaluation.id == evaluation_id,
        CourseEvaluation.student_id == current_user.id
    ).first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="评价记录不存在")

    # 更新字段
    update_data = evaluation_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(evaluation, field, value)

    evaluation.updated_at = datetime.now()
    db.commit()
    db.refresh(evaluation)

    course = db.query(Course).filter(Course.id == evaluation.course_id).first()
    result = build_evaluation_response(evaluation, course, current_user)

    return result


@router.delete("/{evaluation_id}", summary="删除评价")
async def delete_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """学生删除自己的评价"""
    evaluation = db.query(CourseEvaluation).filter(
        CourseEvaluation.id == evaluation_id,
        CourseEvaluation.student_id == current_user.id
    ).first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="评价记录不存在")

    db.delete(evaluation)
    db.commit()

    return {"message": "评价已删除"}


def build_evaluation_response(evaluation: CourseEvaluation, course: Course, user: User) -> dict:
    """构建评价响应数据"""
    return {
        "id": evaluation.id,
        "student_id": evaluation.student_id,
        "student_name": user.real_name or user.username,
        "course_id": evaluation.course_id,
        "course_name": course.course_name if course else "",
        "course_code": course.course_code if course else "",
        "teacher_id": evaluation.teacher_id,
        "teacher_name": course.teacher_name if course else "",
        "semester": evaluation.semester,
        "teaching_quality": evaluation.teaching_quality,
        "course_content": evaluation.course_content,
        "teacher_attitude": evaluation.teacher_attitude,
        "difficulty": evaluation.difficulty,
        "workload": evaluation.workload,
        "overall_rating": evaluation.overall_rating,
        "comment": evaluation.comment,
        "is_recommended": evaluation.is_recommended,
        "created_at": evaluation.created_at
    }
