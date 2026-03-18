from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Classroom, Course, Schedule
from app.schemas import (
    ClassroomCreate, ClassroomUpdate, ClassroomResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    ScheduleCreate, ScheduleUpdate, ScheduleResponse
)

router = APIRouter()


# ========== 教室相关 ==========
@router.get("/classrooms", response_model=List[ClassroomResponse], summary="获取所有教室")
async def get_classrooms(
    building: Optional[str] = Query(None, description="教学楼"),
    room_type: Optional[str] = Query(None, description="教室类型"),
    min_capacity: Optional[int] = Query(None, description="最小容量"),
    db: Session = Depends(get_db)
):
    """获取教室列表，支持筛选"""
    query = db.query(Classroom).filter(Classroom.is_available == 1)

    if building:
        query = query.filter(Classroom.building == building)
    if room_type:
        query = query.filter(Classroom.room_type == room_type)
    if min_capacity:
        query = query.filter(Classroom.capacity >= min_capacity)

    return query.order_by(Classroom.building, Classroom.room_number).all()


@router.get("/classrooms/{classroom_id}", response_model=ClassroomResponse, summary="获取教室详情")
async def get_classroom(classroom_id: int, db: Session = Depends(get_db)):
    """获取单个教室的详细信息"""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="教室不存在")
    return classroom


@router.get("/classrooms/{classroom_id}/schedule", response_model=List[ScheduleResponse], summary="获取教室课表")
async def get_classroom_schedule(
    classroom_id: int,
    semester: Optional[str] = Query(None, description="学期"),
    db: Session = Depends(get_db)
):
    """获取指定教室的课表"""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="教室不存在")

    query = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    ).filter(Schedule.classroom_id == classroom_id)

    if semester:
        query = query.filter(Schedule.semester == semester)

    return query.order_by(Schedule.day_of_week, Schedule.period).all()


@router.get("/classrooms/{classroom_id}/status", summary="获取教室状态")
async def get_classroom_status(
    classroom_id: int,
    day_of_week: int = Query(..., description="星期：1-7"),
    period: int = Query(..., description="节次：1-5"),
    week: int = Query(default=1, description="当前周次"),
    semester: Optional[str] = Query(None, description="学期"),
    db: Session = Depends(get_db)
):
    """获取教室在指定时间的占用状态"""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="教室不存在")

    # 查询该时间段是否有课
    query = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    ).filter(
        Schedule.classroom_id == classroom_id,
        Schedule.day_of_week == day_of_week,
        Schedule.period == period,
        Schedule.week_start <= week,
        Schedule.week_end >= week
    )

    if semester:
        query = query.filter(Schedule.semester == semester)

    occupied_courses = query.all()

    return {
        "classroom": classroom,
        "is_available": len(occupied_courses) == 0 and classroom.is_available == 1,
        "occupied_courses": occupied_courses if occupied_courses else None
    }


@router.get("/available-classrooms", response_model=List[ClassroomResponse], summary="查询空教室")
async def get_available_classrooms(
    day_of_week: int = Query(..., description="星期：1-7"),
    period: int = Query(..., description="节次：1-5"),
    week: int = Query(default=1, description="当前周次"),
    semester: Optional[str] = Query(None, description="学期"),
    building: Optional[str] = Query(None, description="教学楼筛选"),
    min_capacity: Optional[int] = Query(None, description="最小容量筛选"),
    room_type: Optional[str] = Query(None, description="教室类型筛选"),
    db: Session = Depends(get_db)
):
    """查询指定时间段的空闲教室"""
    # 获取所有可用教室
    query = db.query(Classroom).filter(Classroom.is_available == 1)

    if building:
        query = query.filter(Classroom.building == building)
    if room_type:
        query = query.filter(Classroom.room_type == room_type)
    if min_capacity:
        query = query.filter(Classroom.capacity >= min_capacity)

    all_classrooms = query.all()

    # 查询该时间段被占用的教室ID
    occupied_query = db.query(Schedule.classroom_id).filter(
        Schedule.day_of_week == day_of_week,
        Schedule.period == period,
        Schedule.week_start <= week,
        Schedule.week_end >= week
    )

    if semester:
        occupied_query = occupied_query.filter(Schedule.semester == semester)

    occupied_classroom_ids = {row[0] for row in occupied_query.all()}

    # 返回未被占用的教室
    available_classrooms = [
        classroom for classroom in all_classrooms
        if classroom.id not in occupied_classroom_ids
    ]

    return available_classrooms


# ========== 课程相关 ==========
@router.get("/courses", response_model=List[CourseResponse], summary="获取所有课程")
async def get_courses(
    department: Optional[str] = Query(None, description="院系"),
    course_type: Optional[str] = Query(None, description="课程类型"),
    db: Session = Depends(get_db)
):
    """获取课程列表，支持筛选"""
    query = db.query(Course)

    if department:
        query = query.filter(Course.department == department)
    if course_type:
        query = query.filter(Course.course_type == course_type)

    return query.order_by(Course.course_code).all()


@router.get("/courses/{course_id}", response_model=CourseResponse, summary="获取课程详情")
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """获取单个课程的详细信息"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course


@router.get("/courses/{course_id}/schedule", response_model=List[ScheduleResponse], summary="获取课程课表")
async def get_course_schedule(
    course_id: int,
    semester: Optional[str] = Query(None, description="学期"),
    db: Session = Depends(get_db)
):
    """获取指定课程的课表"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    query = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    ).filter(Schedule.course_id == course_id)

    if semester:
        query = query.filter(Schedule.semester == semester)

    return query.order_by(Schedule.day_of_week, Schedule.period).all()


# ========== 排课相关 ==========
@router.get("/schedules", response_model=List[ScheduleResponse], summary="获取排课列表")
async def get_schedules(
    semester: Optional[str] = Query(None, description="学期"),
    day_of_week: Optional[int] = Query(None, description="星期：1-7"),
    period: Optional[int] = Query(None, description="节次：1-5"),
    db: Session = Depends(get_db)
):
    """获取排课列表，支持筛选"""
    query = db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    )

    if semester:
        query = query.filter(Schedule.semester == semester)
    if day_of_week:
        query = query.filter(Schedule.day_of_week == day_of_week)
    if period:
        query = query.filter(Schedule.period == period)

    return query.order_by(Schedule.day_of_week, Schedule.period).all()


@router.get("/buildings", summary="获取所有教学楼")
async def get_buildings(db: Session = Depends(get_db)):
    """获取所有教学楼列表"""
    buildings = db.query(Classroom.building).distinct().all()
    return {"buildings": sorted([b[0] for b in buildings])}


@router.get("/periods", summary="获取所有节次")
async def get_periods():
    """获取所有节次"""
    return {
        "periods": [
            {"value": 1, "label": "第1节", "time": "08:00-09:40"},
            {"value": 2, "label": "第2节", "time": "10:00-11:40"},
            {"value": 3, "label": "第3节", "time": "14:00-15:40"},
            {"value": 4, "label": "第4节", "time": "16:00-17:40"},
            {"value": 5, "label": "第5节", "time": "19:00-20:40"}
        ]
    }


@router.get("/weekdays", summary="获取所有星期")
async def get_weekdays():
    """获取所有星期"""
    return {
        "days": [
            {"value": 1, "label": "周一"},
            {"value": 2, "label": "周二"},
            {"value": 3, "label": "周三"},
            {"value": 4, "label": "周四"},
            {"value": 5, "label": "周五"},
            {"value": 6, "label": "周六"},
            {"value": 7, "label": "周日"}
        ]
    }
