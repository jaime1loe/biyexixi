from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Book, Seat, SeatReservation

router = APIRouter()


# 模拟数据 - 实际项目中应该从学校系统API获取
EMPTY_CLASSROOMS = {
    "教学楼A": ["101", "102", "103", "105", "201", "202", "203"],
    "教学楼B": ["301", "302", "303", "305", "401", "402"],
    "实验楼": ["101", "102", "201", "202"],
}

# 模拟图书馆数据
LIBRARY_DATA = {
    "floors": [
        {"floor": 1, "name": "借阅区", "books_count": 15000},
        {"floor": 2, "name": "自习区", "seats": 200},
        {"floor": 3, "name": "期刊区", "books_count": 5000},
        {"floor": 4, "name": "电子阅览室", "computers": 50},
    ],
    "opening_hours": "周一至周日 8:00-22:00",
    "location": "校园中心区域，东侧主楼",
}


@router.get("/empty-classrooms", summary="查询空教室")
async def get_empty_classrooms(
    building: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """查询当前空教室"""
    result = []
    if building and building in EMPTY_CLASSROOMS:
        result = [{"building": building, "room": room} for room in EMPTY_CLASSROOMS[building]]
    else:
        for building_name, rooms in EMPTY_CLASSROOMS.items():
            for room in rooms:
                result.append({"building": building_name, "room": room})
    return {
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "classrooms": result
    }


@router.get("/library/info", summary="图书馆信息")
async def get_library_info(
    current_user = Depends(get_current_user)
):
    """获取图书馆基本信息"""
    return LIBRARY_DATA


@router.get("/library/books", summary="查询图书馆藏书")
async def search_books(
    keyword: Optional[str] = Query(None, description="搜索关键词（书名或作者）"),
    category: Optional[str] = Query(None, description="图书分类"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """查询图书馆藏书"""
    query = db.query(Book)

    # 关键词搜索（书名或作者）
    if keyword:
        keyword_lower = keyword.lower()
        query = query.filter(
            (Book.title.ilike(f"%{keyword_lower}%")) |
            (Book.author.ilike(f"%{keyword_lower}%"))
        )

    # 分类过滤
    if category:
        query = query.filter(Book.category == category)

    books = query.all()

    # 转换为响应格式
    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "publish_year": book.publish_year,
            "isbn": book.isbn,
            "category": book.category,
            "location": book.location,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "status": book.status,
            "language": book.language,
            "pages": book.pages,
            "price": book.price,
            "description": book.description
        })

    return {
        "total": len(result),
        "books": result
    }


@router.get("/library/categories", summary="图书分类")
async def get_book_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取图书分类"""
    categories = db.query(Book.category).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]
    return {"categories": category_list}


@router.get("/library/books/{book_id}", summary="图书详情")
async def get_book_detail(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取图书详情"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "publish_year": book.publish_year,
        "isbn": book.isbn,
        "category": book.category,
        "location": book.location,
        "total_copies": book.total_copies,
        "available_copies": book.available_copies,
        "status": book.status,
        "language": book.language,
        "pages": book.pages,
        "price": book.price,
        "description": book.description,
        "created_at": book.created_at,
        "updated_at": book.updated_at
    }


@router.get("/library/seats", summary="查询图书馆座位")
async def get_seats(
    floor: Optional[int] = Query(None, description="楼层"),
    area: Optional[str] = Query(None, description="区域"),
    seat_type: Optional[str] = Query(None, description="座位类型"),
    status: Optional[str] = Query(None, description="状态：available/occupied/reserved"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """查询图书馆座位"""
    query = db.query(Seat).filter(Seat.is_available == 1)

    # 楼层过滤
    if floor:
        query = query.filter(Seat.floor == floor)

    # 区域过滤
    if area:
        query = query.filter(Seat.area == area)

    # 座位类型过滤
    if seat_type:
        query = query.filter(Seat.seat_type == seat_type)

    # 状态过滤
    if status:
        query = query.filter(Seat.status == status)

    seats = query.all()

    # 转换为响应格式
    result = []
    for seat in seats:
        result.append({
            "id": seat.id,
            "seat_number": seat.seat_number,
            "floor": seat.floor,
            "area": seat.area,
            "seat_type": seat.seat_type,
            "status": seat.status,
            "is_available": seat.is_available == 1
        })

    # 统计信息
    total_seats = len(result)
    available_seats = len([s for s in result if s["status"] == "available"])
    occupied_seats = len([s for s in result if s["status"] == "occupied"])
    reserved_seats = len([s for s in result if s["status"] == "reserved"])

    return {
        "total": total_seats,
        "available": available_seats,
        "occupied": occupied_seats,
        "reserved": reserved_seats,
        "seats": result
    }


@router.post("/library/seats/{seat_id}/reserve", summary="预约座位")
async def reserve_seat(
    seat_id: int,
    reservation_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """预约座位"""
    # 检查座位是否存在
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")

    # 检查座位是否可用
    if seat.is_available != 1:
        raise HTTPException(status_code=400, detail="座位不可用")

    # 检查座位状态
    if seat.status != "available":
        raise HTTPException(status_code=400, detail=f"座位当前状态为：{seat.status}，无法预约")

    # 检查用户是否已有未使用的预约
    today = date.today().strftime("%Y-%m-%d")
    existing_reservation = db.query(SeatReservation).filter(
        SeatReservation.user_id == current_user.id,
        SeatReservation.reservation_date == today,
        SeatReservation.status.in_(["reserved", "checked_in"])
    ).first()

    if existing_reservation:
        raise HTTPException(status_code=400, detail="您今天已有预约，请先签到或取消")

    # 检查是否已有该日期该座位的预约
    reservation_date = reservation_data.get("reservation_date", today)
    start_time = reservation_data.get("start_time")
    end_time = reservation_data.get("end_time")

    conflicting_reservation = db.query(SeatReservation).filter(
        SeatReservation.seat_id == seat_id,
        SeatReservation.reservation_date == reservation_date,
        SeatReservation.status.in_(["reserved", "checked_in"])
    ).first()

    if conflicting_reservation:
        raise HTTPException(status_code=400, detail="该座位在指定时间段已被预约")

    # 创建预约
    reservation = SeatReservation(
        user_id=current_user.id,
        seat_id=seat_id,
        reservation_date=reservation_date,
        start_time=start_time,
        end_time=end_time,
        status="reserved"
    )

    db.add(reservation)

    # 更新座位状态
    seat.status = "reserved"

    db.commit()

    return {
        "message": "预约成功",
        "reservation_id": reservation.id,
        "seat": {
            "id": seat.id,
            "seat_number": seat.seat_number,
            "floor": seat.floor,
            "area": seat.area
        }
    }


@router.post("/library/seats/{seat_id}/checkin", summary="签到")
async def check_in_seat(
    seat_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """签到"""
    # 查找预约记录
    today = date.today().strftime("%Y-%m-%d")
    reservation = db.query(SeatReservation).filter(
        SeatReservation.user_id == current_user.id,
        SeatReservation.seat_id == seat_id,
        SeatReservation.reservation_date == today,
        SeatReservation.status == "reserved"
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="未找到有效的预约记录")

    # 更新预约状态
    reservation.status = "checked_in"
    reservation.check_in_time = datetime.now()

    # 更新座位状态
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    seat.status = "occupied"

    db.commit()

    return {
        "message": "签到成功",
        "seat": {
            "id": seat.id,
            "seat_number": seat.seat_number,
            "floor": seat.floor,
            "area": seat.area
        }
    }


@router.delete("/library/reservations/{reservation_id}", summary="取消预约")
async def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """取消预约"""
    # 查找预约记录
    reservation = db.query(SeatReservation).filter(
        SeatReservation.id == reservation_id,
        SeatReservation.user_id == current_user.id,
        SeatReservation.status == "reserved"
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="未找到有效的预约记录")

    # 更新预约状态
    reservation.status = "cancelled"

    # 更新座位状态
    seat = db.query(Seat).filter(Seat.id == reservation.seat_id).first()
    seat.status = "available"

    db.commit()

    return {"message": "取消预约成功"}


@router.get("/library/my-reservations", summary="我的预约")
async def get_my_reservations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取我的预约记录"""
    reservations = db.query(SeatReservation).filter(
        SeatReservation.user_id == current_user.id
    ).order_by(SeatReservation.created_at.desc()).limit(10).all()

    result = []
    for r in reservations:
        seat = db.query(Seat).filter(Seat.id == r.seat_id).first()
        result.append({
            "id": r.id,
            "seat_id": r.seat_id,
            "seat_number": seat.seat_number if seat else "",
            "floor": seat.floor if seat else 0,
            "area": seat.area if seat else "",
            "seat_type": seat.seat_type if seat else "",
            "reservation_date": r.reservation_date,
            "start_time": r.start_time,
            "end_time": r.end_time,
            "status": r.status,
            "check_in_time": r.check_in_time,
            "check_out_time": r.check_out_time,
            "created_at": r.created_at
        })

    return {"reservations": result}


@router.get("/library/floors", summary="获取楼层列表")
async def get_library_floors(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取图书馆楼层列表"""
    try:
        floors = db.query(Seat.floor).distinct().all()
        floor_list = [f[0] for f in floors if f[0]]
        return {"floors": sorted(floor_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取楼层列表失败: {str(e)}")


@router.get("/library/areas", summary="获取区域列表")
async def get_library_areas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取图书馆区域列表"""
    try:
        areas = db.query(Seat.area).distinct().all()
        area_list = [a[0] for a in areas if a[0]]
        return {"areas": area_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取区域列表失败: {str(e)}")
