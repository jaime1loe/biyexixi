from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
import shutil
from pathlib import Path

from app.database import get_db
from app.models import Notification
from app.schemas import NotificationCreate, NotificationResponse
from app.dependencies import get_current_admin_user, get_current_user

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = Path("uploads/notifications")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=NotificationResponse, summary="创建通知（仅管理员）")
async def create_notification(
    notification: NotificationCreate,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """创建通知（仅管理员）"""
    file_path = None

    if file:
        # 保存上传的文件
        file_name = f"{notification.title[:50]}_{file.filename}"
        file_name = "".join(c if c.isalnum() or c in (' ', '-', '_', '.') else '_' for c in file_name)
        save_path = UPLOAD_DIR / file_name

        # 确保文件名唯一
        counter = 1
        while save_path.exists():
            name_without_ext = save_path.stem
            file_ext = save_path.suffix
            file_name = f"{name_without_ext}_{counter}{file_ext}"
            save_path = UPLOAD_DIR / file_name
            counter += 1

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_path = str(save_path)

    db_notification = Notification(
        title=notification.title,
        content=notification.content,
        category=notification.category,
        is_important=notification.is_important,
        file_path=file_path
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


@router.get("/", response_model=List[NotificationResponse], summary="获取通知列表")
async def get_notifications(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    is_important: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取通知列表（公开访问）"""
    query = db.query(Notification)

    if category:
        query = query.filter(Notification.category == category)

    if is_important is not None:
        query = query.filter(Notification.is_important == (1 if is_important else 0))

    notifications = query.order_by(
        desc(Notification.is_important),
        desc(Notification.created_at)
    ).offset(skip).limit(limit).all()
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse, summary="获取通知详情")
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取通知详情"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )
    return notification


@router.delete("/{notification_id}", summary="删除通知（仅管理员）")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """删除通知（仅管理员）"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )

    # 删除关联的文件
    if notification.file_path:
        file_path = Path(notification.file_path)
        if file_path.exists():
            file_path.unlink()

    db.delete(notification)
    db.commit()
    return {"message": "删除成功"}


@router.get("/{notification_id}/download", summary="下载通知附件")
async def download_notification_file(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """下载通知关联的附件"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )

    if not notification.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该通知没有附件"
        )

    from fastapi.responses import FileResponse
    file_path = Path(notification.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream"
    )


@router.get("/categories/list", summary="获取通知分类列表")
async def get_notification_categories(db: Session = Depends(get_db)):
    """获取所有通知分类"""
    categories = db.query(Notification.category).distinct().all()
    return {"categories": [c[0] for c in categories if c[0]]}
