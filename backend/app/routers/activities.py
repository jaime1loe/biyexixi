from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List

from app.database import get_db
from app.models import ActivityLog, User
from app.schemas import ActivityLogResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ActivityLogResponse], summary="获取活动记录列表")
async def get_activities(
    skip: int = 0,
    limit: int = 20,
    action_type: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取活动记录列表"""
    query = db.query(ActivityLog).options(joinedload(ActivityLog.user))
    
    if action_type:
        query = query.filter(ActivityLog.action_type == action_type)
    
    activities = query.order_by(desc(ActivityLog.created_at)).offset(skip).limit(limit).all()
    
    # 填充用户信息
    result = []
    for activity in activities:
        activity_dict = {
            "id": activity.id,
            "user_id": activity.user_id,
            "username": activity.user.username if activity.user else None,
            "user_role": activity.user.role if activity.user else None,
            "action_type": activity.action_type,
            "target_type": activity.target_type,
            "target_id": activity.target_id,
            "target_name": activity.target_name,
            "details": activity.details,
            "created_at": activity.created_at
        }
        result.append(ActivityLogResponse(**activity_dict))
    
    return result


@router.get("/recent", response_model=List[ActivityLogResponse], summary="获取最近活动")
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取最近的活动记录"""
    activities = db.query(ActivityLog).options(joinedload(ActivityLog.user)).order_by(
        desc(ActivityLog.created_at)
    ).limit(limit).all()
    
    result = []
    for activity in activities:
        activity_dict = {
            "id": activity.id,
            "user_id": activity.user_id,
            "username": activity.user.username if activity.user else None,
            "user_role": activity.user.role if activity.user else None,
            "action_type": activity.action_type,
            "target_type": activity.target_type,
            "target_id": activity.target_id,
            "target_name": activity.target_name,
            "details": activity.details,
            "created_at": activity.created_at
        }
        result.append(ActivityLogResponse(**activity_dict))
    
    return result


def log_activity(
    db: Session,
    user_id: int,
    action_type: str,
    target_type: str = None,
    target_id: int = None,
    target_name: str = None,
    details: str = None,
    ip_address: str = None
):
    """记录活动"""
    activity = ActivityLog(
        user_id=user_id,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        target_name=target_name,
        details=details,
        ip_address=ip_address
    )
    db.add(activity)
    db.commit()
