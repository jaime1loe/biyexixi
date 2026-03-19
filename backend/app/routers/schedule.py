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
from app.dependencies import get_current_user

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


# ========== 排课CRUD操作 ==========
@router.post("/schedules", response_model=ScheduleResponse, summary="创建排课")
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员创建排课"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以创建排课")

    # 检查课程是否存在
    course = db.query(Course).filter(Course.id == schedule_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 检查教室是否存在
    classroom = db.query(Classroom).filter(Classroom.id == schedule_data.classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="教室不存在")

    # 检查教室容量是否足够
    if classroom.capacity < course.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"教室容量不足（教室容量：{classroom.capacity}，课程容量：{course.capacity}）"
        )

    # 检查时间冲突
    conflict = db.query(Schedule).filter(
        Schedule.classroom_id == schedule_data.classroom_id,
        Schedule.day_of_week == schedule_data.day_of_week,
        Schedule.period == schedule_data.period,
        Schedule.semester == schedule_data.semester,
        Schedule.week_start <= schedule_data.week_end,
        Schedule.week_end >= schedule_data.week_start
    ).first()

    if conflict:
        raise HTTPException(
            status_code=400,
            detail=f"时间冲突：教室{classroom.building}{classroom.room_number}在该时段已有排课"
        )

    # 创建排课
    db_schedule = Schedule(
        classroom_id=schedule_data.classroom_id,
        course_id=schedule_data.course_id,
        day_of_week=schedule_data.day_of_week,
        period=schedule_data.period,
        week_start=schedule_data.week_start,
        week_end=schedule_data.week_end,
        semester=schedule_data.semester,
        class_name=schedule_data.class_name
    )

    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)

    # 记录活动日志
    from app.routers.activities import log_activity
    log_activity(
        db,
        user_id=current_user.id,
        action_type="创建排课",
        target_type="schedule",
        target_id=db_schedule.id,
        target_name=f"{course.course_name} - {classroom.building}{classroom.room_number}",
        details=f"为课程 {course.course_name} 创建排课：{classroom.building}{classroom.room_number} {get_weekday_label(schedule_data.day_of_week)} 第{schedule_data.period}节"
    )

    # 重新查询以获取关联数据
    return db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    ).filter(Schedule.id == db_schedule.id).first()


@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse, summary="更新排课")
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员更新排课"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以更新排课")

    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="排课不存在")

    # 如果修改了教室，检查教室是否存在
    if schedule_data.classroom_id is not None:
        classroom = db.query(Classroom).filter(Classroom.id == schedule_data.classroom_id).first()
        if not classroom:
            raise HTTPException(status_code=404, detail="教室不存在")

        # 检查教室容量
        if classroom.id != db_schedule.classroom_id:
            course = db.query(Course).filter(Course.id == db_schedule.course_id).first()
            if classroom.capacity < course.capacity:
                raise HTTPException(
                    status_code=400,
                    detail=f"教室容量不足（教室容量：{classroom.capacity}，课程容量：{course.capacity}）"
                )

    # 检查时间冲突（排除自己）
    conflict = db.query(Schedule).filter(
        Schedule.id != schedule_id,
        Schedule.classroom_id == schedule_data.classroom_id if schedule_data.classroom_id is not None else Schedule.classroom_id == db_schedule.classroom_id,
        Schedule.day_of_week == schedule_data.day_of_week if schedule_data.day_of_week is not None else Schedule.day_of_week == db_schedule.day_of_week,
        Schedule.period == schedule_data.period if schedule_data.period is not None else Schedule.period == db_schedule.period,
        Schedule.semester == schedule_data.semester if schedule_data.semester is not None else Schedule.semester == db_schedule.semester,
        Schedule.week_start <= schedule_data.week_end if schedule_data.week_end is not None else True,
        Schedule.week_end >= schedule_data.week_start if schedule_data.week_start is not None else True
    ).first()

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="时间冲突：该教室在该时段已有排课"
        )

    # 更新字段
    if schedule_data.classroom_id is not None:
        db_schedule.classroom_id = schedule_data.classroom_id
    if schedule_data.course_id is not None:
        db_schedule.course_id = schedule_data.course_id
    if schedule_data.day_of_week is not None:
        db_schedule.day_of_week = schedule_data.day_of_week
    if schedule_data.period is not None:
        db_schedule.period = schedule_data.period
    if schedule_data.week_start is not None:
        db_schedule.week_start = schedule_data.week_start
    if schedule_data.week_end is not None:
        db_schedule.week_end = schedule_data.week_end
    if schedule_data.semester is not None:
        db_schedule.semester = schedule_data.semester
    if schedule_data.class_name is not None:
        db_schedule.class_name = schedule_data.class_name

    db_schedule.updated_at = datetime.now()
    db.commit()
    db.refresh(db_schedule)

    # 记录活动日志
    from app.routers.activities import log_activity
    log_activity(
        db,
        user_id=current_user.id,
        action_type="更新排课",
        target_type="schedule",
        target_id=db_schedule.id,
        target_name=f"{db_schedule.course.course_name if db_schedule.course else ''}",
        details="更新排课信息"
    )

    # 重新查询以获取关联数据
    return db.query(Schedule).options(
        joinedload(Schedule.course),
        joinedload(Schedule.classroom)
    ).filter(Schedule.id == db_schedule.id).first()


@router.delete("/schedules/{schedule_id}", summary="删除排课")
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """管理员删除排课"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以删除排课")

    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="排课不存在")

    # 记录活动日志
    from app.routers.activities import log_activity
    course_name = db_schedule.course.course_name if db_schedule.course else ""
    classroom_info = f"{db_schedule.classroom.building}{db_schedule.classroom.room_number}" if db_schedule.classroom else ""

    log_activity(
        db,
        user_id=current_user.id,
        action_type="删除排课",
        target_type="schedule",
        target_id=db_schedule.id,
        target_name=f"{course_name} - {classroom_info}",
        details=f"删除排课：{course_name} {classroom_info}"
    )

    db.delete(db_schedule)
    db.commit()

    return {"message": "删除成功"}


def get_weekday_label(day: int) -> str:
    """获取星期标签"""
    weekdays = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
    return weekdays.get(day, "")
