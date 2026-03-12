from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc

from app.database import get_db
from app.models import Favorite, Question, User
from app.schemas import FavoriteCreate, FavoriteResponse, QuestionResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=FavoriteResponse, summary="收藏问题")
async def create_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """收藏问题"""
    # 检查问题是否存在
    question = db.query(Question).filter(Question.id == favorite.question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )

    # 检查是否已收藏
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == favorite.question_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过了"
        )

    db_favorite = Favorite(
        user_id=current_user.id,
        question_id=favorite.question_id
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)

    return db_favorite


@router.delete("/{favorite_id}", summary="取消收藏")
async def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """取消收藏"""
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )

    if favorite.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权取消他人的收藏"
        )

    db.delete(favorite)
    db.commit()
    return {"message": "取消收藏成功"}


@router.get("/", response_model=List[FavoriteResponse], summary="获取我的收藏列表")
async def get_my_favorites(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取当前用户的收藏列表"""
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).order_by(desc(Favorite.created_at)).offset(skip).limit(limit).all()
    
    # 构建响应数据，包含问题和回答内容
    favorite_responses = []
    for favorite in favorites:
        question = db.query(Question).filter(Question.id == favorite.question_id).first()
        if question:
            favorite_data = {
                "id": favorite.id,
                "user_id": favorite.user_id,
                "question_id": favorite.question_id,
                "created_at": favorite.created_at,
                "question": question.question,
                "answer": question.answer
            }
            favorite_responses.append(favorite_data)
    
    return favorite_responses


@router.get("/check/{question_id}", summary="检查是否已收藏")
async def check_favorite(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """检查某个问题是否已被当前用户收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()
    return {"is_favorited": favorite is not None}
