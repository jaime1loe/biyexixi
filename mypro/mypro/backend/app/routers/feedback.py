from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc

from app.database import get_db
from app.models import Feedback
from app.schemas import FeedbackCreate, FeedbackResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=FeedbackResponse, summary="提交反馈")
async def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提交反馈评价"""
    # 检查是否已评价过该问题
    existing_feedback = db.query(Feedback).filter(
        Feedback.user_id == current_user.id,
        Feedback.question_id == feedback.question_id
    ).first()
    
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已经评价过该问题"
        )

    db_feedback = Feedback(
        user_id=current_user.id,
        question_id=feedback.question_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    return db_feedback


@router.get("/my", response_model=List[FeedbackResponse], summary="获取我的反馈列表")
async def get_my_feedbacks(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取当前用户的反馈列表"""
    feedbacks = db.query(Feedback).filter(
        Feedback.user_id == current_user.id
    ).order_by(desc(Feedback.created_at)).offset(skip).limit(limit).all()
    return feedbacks


@router.get("/question/{question_id}", response_model=List[FeedbackResponse], summary="获取问题的反馈列表")
async def get_question_feedbacks(
    question_id: int,
    db: Session = Depends(get_db)
):
    """获取某个问题的所有反馈"""
    feedbacks = db.query(Feedback).filter(
        Feedback.question_id == question_id
    ).order_by(desc(Feedback.created_at)).all()
    return feedbacks


@router.get("/", response_model=List[FeedbackResponse], summary="获取反馈列表")
async def get_feedbacks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取反馈列表"""
    feedbacks = db.query(Feedback).order_by(desc(Feedback.created_at)).offset(skip).limit(limit).all()
    return feedbacks
