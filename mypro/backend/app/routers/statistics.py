from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, desc, func
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models import Question, User, Feedback
from app.schemas import StatisticsResponse
from app.dependencies import get_current_admin_user

router = APIRouter()


@router.get("/overview", summary="获取数据概览")
async def get_statistics_overview(db: Session = Depends(get_db)):
    """获取数据概览统计"""
    # 问题总数
    total_questions = db.query(func.count(Question.id)).scalar() or 0

    # 总回答数（有答案的问题数量）
    total_answers = db.query(func.count(Question.id)).filter(
        Question.answer.isnot(None),
        Question.answer != ""
    ).scalar() or 0

    # 总提问次数（所有问题的ask_count总和）
    total_ask_count = db.query(func.sum(Question.ask_count)).scalar() or 0

    # 用户总数
    total_users = db.query(func.count(User.id)).scalar() or 0

    # 知识库总数
    from app.models import Knowledge
    total_knowledge = db.query(func.count(Knowledge.id)).scalar() or 0

    # 平均评分
    avg_rating = db.query(func.avg(Feedback.rating)).scalar() or 0

    # 今日问题数
    today_questions = db.query(func.count(Question.id)).filter(
        text("DATE(created_at) = CURDATE()")
    ).scalar() or 0

    # 今日活跃用户数
    today_users = db.query(func.count(func.distinct(Question.user_id))).filter(
        text("DATE(created_at) = CURDATE()")
    ).scalar() or 0

    # 本周问题数
    week_ago = datetime.now() - timedelta(days=7)
    week_questions = db.query(func.count(Question.id)).filter(
        Question.created_at >= week_ago
    ).scalar() or 0

    return {
        "question_count": total_questions,
        "answer_count": total_answers,
        "ask_count": total_ask_count,
        "user_count": total_users,
        "knowledge_count": total_knowledge,
        "avg_rating": round(float(avg_rating), 2) if avg_rating else 0,
        "today_questions": today_questions,
        "today_users": today_users,
        "week_questions": week_questions
    }


@router.get("/daily", response_model=List[StatisticsResponse], summary="获取每日统计")
async def get_daily_statistics(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取每日统计数据"""
    stats = []
    for i in range(days):
        date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        
        # 查询当天的统计数据
        question_count = db.query(func.count(Question.id)).filter(
            text(f"DATE(created_at) = '{date_str}'")
        ).scalar() or 0
        
        user_count = db.query(func.count(func.distinct(Question.user_id))).filter(
            text(f"DATE(created_at) = '{date_str}'")
        ).scalar() or 0
        
        avg_rating = db.query(func.avg(Feedback.rating)).filter(
            text(f"DATE(created_at) = '{date_str}'")
        ).scalar() or 0
        
        stats.append(StatisticsResponse(
            date=date_str,
            question_count=question_count,
            user_count=user_count,
            avg_rating=round(float(avg_rating), 2) if avg_rating else 0.0
        ))
    
    # 反转列表，使日期从早到晚
    return list(reversed(stats))


@router.get("/category", summary="获取分类统计")
async def get_category_statistics(db: Session = Depends(get_db)):
    """获取问题分类统计"""
    from sqlalchemy import and_
    
    results = db.query(
        Question.category,
        func.count(Question.id).label('count')
    ).filter(
        Question.category.isnot(None)
    ).group_by(Question.category).all()
    
    categories = [{"category": r[0], "count": r[1]} for r in results]
    return {"categories": categories}


@router.get("/top-questions", summary="获取热门问题")
async def get_top_questions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取热门问题（按提问次数倒序）"""
    try:
        # 按提问次数排序，获取热门问题
        questions = db.query(Question).order_by(
            desc(Question.ask_count)
        ).limit(limit).all()

        # 格式化返回数据
        result = []
        for q in questions:
            result.append({
                "id": q.id,
                "question": q.question,
                "answer": q.answer,
                "ask_count": q.ask_count or 1,
                "views": getattr(q, 'views', 0) or 0,
                "created_at": q.created_at.isoformat() if q.created_at else ""
            })
        
        return result
    except Exception as e:
        print(f"获取热门问题出错: {e}")
        return []
