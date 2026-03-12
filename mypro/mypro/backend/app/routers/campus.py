from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()


# 模拟数据 - 实际项目中应该从学校系统API获取
EMPTY_CLASSROOMS = {
    "教学楼A": ["101", "102", "103", "105", "201", "202", "203"],
    "教学楼B": ["301", "302", "303", "305", "401", "402"],
    "实验楼": ["101", "102", "201", "202"],
}

# 模拟成绩数据
GRADES_DATA = {
    "student1": [
        {"course": "高等数学", "score": 85, "credit": 4, "semester": "2023-2024-1"},
        {"course": "大学英语", "score": 92, "credit": 3, "semester": "2023-2024-1"},
        {"course": "计算机基础", "score": 88, "credit": 3, "semester": "2023-2024-1"},
        {"course": "线性代数", "score": 78, "credit": 3, "semester": "2023-2024-2"},
        {"course": "数据结构", "score": 90, "credit": 4, "semester": "2023-2024-2"},
    ],
    "student2": [
        {"course": "高等数学", "score": 76, "credit": 4, "semester": "2023-2024-1"},
        {"course": "大学英语", "score": 85, "credit": 3, "semester": "2023-2024-1"},
        {"course": "计算机基础", "score": 82, "credit": 3, "semester": "2023-2024-1"},
    ],
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

# 模拟图书数据
BOOKS_DATA = [
    {"id": 1, "title": "Python编程从入门到实践", "author": "Eric Matthes", "category": "编程", "location": "一楼A区", "available": True},
    {"id": 2, "title": "深度学习", "author": "Ian Goodfellow", "category": "人工智能", "location": "三楼B区", "available": False},
    {"id": 3, "title": "算法导论", "author": "Thomas H. Cormen", "category": "计算机科学", "location": "一楼A区", "available": True},
    {"id": 4, "title": "机器学习实战", "author": "Peter Harrington", "category": "人工智能", "location": "三楼B区", "available": True},
    {"id": 5, "title": "数据结构与算法分析", "author": "Mark Allen Weiss", "category": "计算机科学", "location": "一楼A区", "available": False},
]


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


@router.get("/grades", summary="查询学习成绩")
async def get_grades(
    current_user = Depends(get_current_user)
):
    """查询当前学生的成绩"""
    username = current_user.username
    grades = GRADES_DATA.get(username, [])

    # 计算平均分
    if grades:
        avg_score = sum(g["score"] for g in grades) / len(grades)
        total_credits = sum(g["credit"] for g in grades)
        weighted_score = sum(g["score"] * g["credit"] for g in grades) / total_credits if total_credits > 0 else 0
    else:
        avg_score = 0
        total_credits = 0
        weighted_score = 0

    return {
        "student_name": current_user.real_name or username,
        "student_id": current_user.student_id,
        "grades": grades,
        "summary": {
            "total_courses": len(grades),
            "average_score": round(avg_score, 2),
            "weighted_score": round(weighted_score, 2),
            "total_credits": total_credits
        }
    }


@router.get("/library/info", summary="图书馆信息")
async def get_library_info(
    current_user = Depends(get_current_user)
):
    """获取图书馆基本信息"""
    return LIBRARY_DATA


@router.get("/library/books", summary="查询图书馆藏书")
async def search_books(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """查询图书馆藏书"""
    books = BOOKS_DATA.copy()

    if keyword:
        keyword_lower = keyword.lower()
        books = [b for b in books if keyword_lower in b["title"].lower() or keyword_lower in b["author"].lower()]

    if category:
        books = [b for b in books if b["category"] == category]

    return {
        "total": len(books),
        "books": books
    }


@router.get("/library/categories", summary="图书分类")
async def get_book_categories(
    current_user = Depends(get_current_user)
):
    """获取图书分类"""
    categories = list(set(b["category"] for b in BOOKS_DATA))
    return {"categories": categories}


@router.get("/library/books/{book_id}", summary="图书详情")
async def get_book_detail(
    book_id: int,
    current_user = Depends(get_current_user)
):
    """获取图书详情"""
    book = next((b for b in BOOKS_DATA if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    return book
