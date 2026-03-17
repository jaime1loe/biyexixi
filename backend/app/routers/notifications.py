from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
import shutil
from pathlib import Path
from datetime import datetime

from app.database import get_db
from app.models import Notification
from app.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from app.dependencies import get_current_admin_user, get_current_user

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = Path("uploads/notifications")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=NotificationResponse, summary="创建通知（仅管理员）")
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """创建通知（仅管理员，JSON格式）"""
    # 确定状态和发布时间
    if notification.schedule_time:
        status = "scheduled"
        published_at = None
    else:
        status = notification.status or "published"
        published_at = datetime.now() if status == "published" else None

    db_notification = Notification(
        title=notification.title,
        content=notification.content,
        detail_content=notification.detail_content,
        category=notification.category,
        is_important=notification.is_important,
        file_path=None,
        publisher=notification.publisher,
        schedule_time=notification.schedule_time,
        status=status,
        published_at=published_at
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


@router.post("/upload", response_model=NotificationResponse, summary="创建通知并上传附件（仅管理员）")
async def create_notification_with_file(
    notification_json: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """创建通知并上传附件（仅管理员）"""
    import json

    # 解析JSON数据
    notification = NotificationCreate(**json.loads(notification_json))

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

    # 确定状态和发布时间
    if notification.schedule_time:
        status = "scheduled"
        published_at = None
    else:
        status = notification.status or "published"
        published_at = datetime.now() if status == "published" else None

    db_notification = Notification(
        title=notification.title,
        content=notification.content,
        detail_content=notification.detail_content,
        category=notification.category,
        is_important=notification.is_important,
        file_path=file_path,
        publisher=notification.publisher,
        schedule_time=notification.schedule_time,
        status=status,
        published_at=published_at
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
    status: Optional[str] = None,
    include_scheduled: bool = False,
    db: Session = Depends(get_db)
):
    """获取通知列表（公开访问）"""
    query = db.query(Notification)

    # 默认只显示已发布的通知，除非指定要包含定时通知
    if not include_scheduled:
        query = query.filter(Notification.status == "published")

    if status:
        query = query.filter(Notification.status == status)

    if category:
        query = query.filter(Notification.category == category)

    if is_important is not None:
        query = query.filter(Notification.is_important == (1 if is_important else 0))

    # 按照重要性、创建时间倒序排序
    notifications = query.order_by(
        desc(Notification.is_important),
        desc(Notification.created_at)
    ).offset(skip).limit(limit).all()
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse, summary="获取通知详情")
@router.get("/{notification_id}/", response_model=NotificationResponse, summary="获取通知详情")
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """获取通知详情（公开访问）"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )
    # 增加浏览次数
    notification.views = (notification.views or 0) + 1
    db.commit()
    db.refresh(notification)
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse, summary="编辑通知（仅管理员）")
@router.put("/{notification_id}/", response_model=NotificationResponse, summary="编辑通知（仅管理员）")
async def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """编辑通知（仅管理员）"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )

    # 更新字段
    if notification_update.title is not None:
        notification.title = notification_update.title
    if notification_update.content is not None:
        notification.content = notification_update.content
    if notification_update.detail_content is not None:
        notification.detail_content = notification_update.detail_content
    if notification_update.category is not None:
        notification.category = notification_update.category
    if notification_update.is_important is not None:
        notification.is_important = notification_update.is_important
    if notification_update.publisher is not None:
        notification.publisher = notification_update.publisher
    if notification_update.schedule_time is not None:
        notification.schedule_time = notification_update.schedule_time
        # 如果设置了定时发布时间，状态设为scheduled
        notification.status = "scheduled"
        notification.published_at = None
    if notification_update.status is not None:
        notification.status = notification_update.status
        # 如果状态改为published且没有发布时间，设置发布时间
        if notification_update.status == "published" and notification.published_at is None:
            notification.published_at = datetime.now()
            # 清除定时时间
            notification.schedule_time = None

    db.commit()
    db.refresh(notification)
    return notification


@router.post("/{notification_id}/upload", response_model=NotificationResponse, summary="编辑通知并上传附件（仅管理员）")
@router.post("/{notification_id}/upload/", response_model=NotificationResponse, summary="编辑通知并上传附件（仅管理员）")
async def update_notification_with_file(
    notification_id: int,
    notification_update: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """编辑通知并上传附件（仅管理员）"""
    import json
    from fastapi import Form

    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )

    # 解析JSON数据
    update_data = json.loads(notification_update)

    # 更新字段
    if 'title' in update_data and update_data['title'] is not None:
        notification.title = update_data['title']
    if 'content' in update_data and update_data['content'] is not None:
        notification.content = update_data['content']
    if 'detail_content' in update_data and update_data['detail_content'] is not None:
        notification.detail_content = update_data['detail_content']
    if 'category' in update_data and update_data['category'] is not None:
        notification.category = update_data['category']
    if 'is_important' in update_data and update_data['is_important'] is not None:
        notification.is_important = update_data['is_important']
    if 'publisher' in update_data and update_data['publisher'] is not None:
        notification.publisher = update_data['publisher']
    if 'schedule_time' in update_data and update_data['schedule_time'] is not None:
        from datetime import datetime
        notification.schedule_time = datetime.fromisoformat(update_data['schedule_time']) if update_data['schedule_time'] else None
        # 如果设置了定时发布时间，状态设为scheduled
        notification.status = "scheduled"
        notification.published_at = None
    if 'status' in update_data and update_data['status'] is not None:
        notification.status = update_data['status']
        # 如果状态改为published且没有发布时间，设置发布时间
        if update_data['status'] == "published" and notification.published_at is None:
            notification.published_at = datetime.now()
            # 清除定时时间
            notification.schedule_time = None

    # 处理文件上传
    if file:
        # 删除旧文件
        if notification.file_path:
            old_file = Path(notification.file_path)
            if old_file.exists():
                old_file.unlink()

        # 保存新文件
        file_name = f"{update_data.get('title', '')[:50]}_{file.filename}"
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

        notification.file_path = str(save_path)

    db.commit()
    db.refresh(notification)
    return notification


@router.delete("/{notification_id}", summary="删除通知（仅管理员）")
@router.delete("/{notification_id}/", summary="删除通知（仅管理员）")
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
@router.get("/{notification_id}/download/", summary="下载通知附件")
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


@router.get("/scheduled/list", response_model=List[NotificationResponse], summary="获取待定时发布的通知列表（仅管理员）")
async def get_scheduled_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """获取所有待定时发布的通知"""
    notifications = db.query(Notification).filter(
        Notification.status == "scheduled"
    ).order_by(Notification.schedule_time).all()
    return notifications


@router.post("/publish/scheduled", summary="发布定时到期的通知（系统调用）")
async def publish_scheduled_notifications(db: Session = Depends(get_db)):
    """发布定时到期的通知（定时任务调用）"""
    now = datetime.now()
    scheduled_notifications = db.query(Notification).filter(
        Notification.status == "scheduled",
        Notification.schedule_time <= now
    ).all()

    count = 0
    for notification in scheduled_notifications:
        notification.status = "published"
        notification.published_at = now
        count += 1

    if count > 0:
        db.commit()

    return {"message": f"已发布 {count} 条定时通知", "count": count}
