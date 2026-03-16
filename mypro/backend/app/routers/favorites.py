from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Question, Favorite
from app.schemas import FavoriteCreate, FavoriteResponse

router = APIRouter()

@router.post("/", response_model=FavoriteResponse)
async def create_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加收藏"""
    # 检查问题是否存在
    question = db.query(Question).filter(Question.id == favorite_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")

    # 检查是否已经收藏
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == favorite_data.question_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="已经收藏过此问题")

    # 创建收藏
    favorite = Favorite(
        user_id=current_user.id,
        question_id=favorite_data.question_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return FavoriteResponse(
        id=favorite.id,
        user_id=favorite.user_id,
        question_id=favorite.question_id,
        question=question.question,
        answer=question.answer,
        created_at=favorite.created_at
    )

@router.get("/", response_model=List[FavoriteResponse])
async def get_favorites(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的收藏列表"""
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).offset(skip).limit(limit).all()
    result = []
    for fav in favorites:
        question = db.query(Question).filter(Question.id == fav.question_id).first()
        if question:
            result.append(FavoriteResponse(
                id=fav.id,
                user_id=fav.user_id,
                question_id=fav.question_id,
                question=question.question,
                answer=question.answer,
                created_at=fav.created_at
            ))
    return result

@router.delete("/{favorite_id}")
async def delete_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == current_user.id
    ).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="收藏记录不存在")

    db.delete(favorite)
    db.commit()
    return {"message": "删除成功"}

@router.get("/check/{question_id}")
async def check_favorite(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查问题是否已收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()
    return {"is_favorited": favorite is not None}
