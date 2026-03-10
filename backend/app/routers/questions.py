from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import get_db
from app.models import Question
from app.schemas import QuestionCreate, QuestionResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=QuestionResponse, summary="提问")
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """用户提问接口"""
    # 创建问题记录
    db_question = Question(
        user_id=current_user.id,
        question=question.question,
        category=question.category
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # 这里可以调用AI服务生成答案
    # 暂时返回占位答案
    db_question.answer = "这是一个示例答案。AI功能将在后续阶段实现。"
    db.commit()
    db.refresh(db_question)

    return db_question


@router.get("/my", response_model=List[QuestionResponse], summary="获取我的问题列表")
async def get_my_questions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取当前用户的问题列表"""
    questions = db.query(Question).filter(
        Question.user_id == current_user.id
    ).order_by(desc(Question.created_at)).offset(skip).limit(limit).all()
    return questions


@router.get("/", response_model=List[QuestionResponse], summary="获取问题列表")
async def get_questions(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取问题列表（公开）"""
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    questions = query.order_by(desc(Question.created_at)).offset(skip).limit(limit).all()
    return questions


@router.get("/{question_id}", response_model=QuestionResponse, summary="获取问题详情")
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """获取问题详情"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    return question
