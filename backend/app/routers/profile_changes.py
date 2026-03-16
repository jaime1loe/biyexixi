from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import User, ProfileChangeRequest
from app.schemas import ProfileChangeCreate, ProfileChangeResponse, ProfileChangeReview
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/profile-changes", tags=["profile-changes"])


@router.post("/submit", response_model=ProfileChangeResponse)
def submit_profile_change(
    change: ProfileChangeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交个人信息修改申请"""
    # 检查是否有待审核的申请
    pending = db.query(ProfileChangeRequest).filter(
        ProfileChangeRequest.user_id == current_user.id,
        ProfileChangeRequest.status == "pending"
    ).first()
    
    if pending:
        raise HTTPException(status_code=400, detail="您有待审核的修改申请，请等待审核结果")
    
    new_change = ProfileChangeRequest(
        user_id=current_user.id,
        **change.dict()
    )
    db.add(new_change)
    db.commit()
    db.refresh(new_change)
    return new_change


@router.get("/my-requests", response_model=List[ProfileChangeResponse])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的修改申请记录"""
    requests = db.query(ProfileChangeRequest).filter(
        ProfileChangeRequest.user_id == current_user.id
    ).order_by(ProfileChangeRequest.created_at.desc()).all()
    return requests


@router.get("/pending", response_model=List[ProfileChangeResponse])
def get_pending_requests(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """获取所有待审核的申请（管理员）"""
    requests = db.query(ProfileChangeRequest).filter(
        ProfileChangeRequest.status == "pending"
    ).order_by(ProfileChangeRequest.created_at.desc()).all()
    return requests


@router.get("/all", response_model=List[ProfileChangeResponse])
def get_all_requests(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """获取所有修改申请（管理员）"""
    query = db.query(ProfileChangeRequest)
    
    if status:
        query = query.filter(ProfileChangeRequest.status == status)
    
    requests = query.order_by(ProfileChangeRequest.created_at.desc()).offset(skip).limit(limit).all()
    return requests


@router.post("/review/{request_id}", response_model=ProfileChangeResponse)
def review_change(
    request_id: int,
    review: ProfileChangeReview,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """审核修改申请（管理员）"""
    change_request = db.query(ProfileChangeRequest).filter(
        ProfileChangeRequest.id == request_id
    ).first()
    
    if not change_request:
        raise HTTPException(status_code=404, detail="申请不存在")
    
    if change_request.status != "pending":
        raise HTTPException(status_code=400, detail="该申请已被审核")
    
    # 更新申请状态
    change_request.status = review.status
    change_request.admin_comment = review.admin_comment
    change_request.reviewed_by = admin.id
    
    # 如果审核通过，更新用户信息
    if review.status == "approved":
        user = db.query(User).filter(User.id == change_request.user_id).first()
        if user:
            if change_request.real_name:
                user.real_name = change_request.real_name
            if change_request.email:
                user.email = change_request.email
            if change_request.phone:
                user.phone = change_request.phone
            if change_request.department:
                user.department = change_request.department
            if change_request.major:
                user.major = change_request.major
            if change_request.bio:
                user.bio = change_request.bio
    
    db.commit()
    db.refresh(change_request)
    return change_request
