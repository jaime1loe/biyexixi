from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
import shutil
from pathlib import Path
import json

from app.database import get_db
from app.models import Knowledge
from app.schemas import KnowledgeCreate, KnowledgeResponse, ReviewAction
from app.models import User
from app.dependencies import get_current_admin_user, get_current_user
from app.config import settings
from app.routers.activities import log_activity

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = Path("uploads/knowledge")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 内存中的分类列表（也可以持久化到数据库）
CATEGORIES = set(["常见问题", "校园指南", "课程资料", "规章制度", "其他"])


@router.post("/", response_model=KnowledgeResponse, summary="添加知识")
async def create_knowledge(
    knowledge: KnowledgeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """添加知识到知识库（仅管理员）"""
    db_knowledge = Knowledge(
        title=knowledge.title,
        content=knowledge.content,
        category=knowledge.category,
        tags=knowledge.tags
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)

    # 这里可以触发向量化处理
    # vector_service.vectorize_knowledge(db_knowledge)

    return db_knowledge


@router.post("/upload", response_model=KnowledgeResponse, summary="上传文件并添加知识")
async def upload_knowledge_file(
    title: str = Form(...),
    content: str = Form(...),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传文件并添加知识（学生、教师、管理员均可上传）"""
    file_path = None
    file_name = None
    file_type = None
    file_size = 0

    if file:
        # 保存上传的文件
        file_ext = file.filename.split(".")[-1] if "." in file.filename else ""
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
        file_name = f"{safe_title[:50]}_{file.filename}"
        save_path = UPLOAD_DIR / file_name

        # 确保文件名唯一
        counter = 1
        while save_path.exists():
            name_without_ext = save_path.stem
            file_name = f"{name_without_ext}_{counter}.{file_ext}" if file_ext else f"{name_without_ext}_{counter}"
            save_path = UPLOAD_DIR / file_name
            counter += 1

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = save_path.stat().st_size
        file_path = str(save_path)
        file_type = file_ext

    # 非管理员上传的内容需要审核
    is_admin = current_user.role == "admin"
    db_knowledge = Knowledge(
        title=title,
        content=content,
        category=category,
        tags=tags,
        status="pending",  # 初始状态为待处理
        review_status="approved" if is_admin else "pending",  # 管理员直接通过，其他需要审核
        uploader_id=current_user.id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    
    # 记录活动
    action_text = f"上传了文件：{file_name}" if file else "添加了知识"
    log_activity(
        db=db,
        user_id=current_user.id,
        action_type="上传文件",
        target_type="knowledge",
        target_id=db_knowledge.id,
        target_name=db_knowledge.title,
        details=action_text
    )

    return db_knowledge


@router.put("/{knowledge_id}", response_model=KnowledgeResponse, summary="更新知识")
async def update_knowledge(
    knowledge_id: int,
    knowledge: KnowledgeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """更新知识（仅管理员）"""
    db_knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not db_knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )
    
    db_knowledge.title = knowledge.title
    db_knowledge.content = knowledge.content
    db_knowledge.category = knowledge.category
    db_knowledge.tags = knowledge.tags
    
    db.commit()
    db.refresh(db_knowledge)
    
    return db_knowledge


@router.get("/search", response_model=List[KnowledgeResponse], summary="搜索知识")
async def search_knowledges(
    keyword: str,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """搜索知识库"""
    query = db.query(Knowledge)
    
    if keyword:
        query = query.filter(
            (Knowledge.title.contains(keyword)) | 
            (Knowledge.content.contains(keyword))
        )
    
    if category:
        query = query.filter(Knowledge.category == category)
    
    knowledges = query.order_by(desc(Knowledge.created_at)).all()
    return knowledges


@router.get("/categories", summary="获取所有分类")
async def get_categories(db: Session = Depends(get_db)):
    """获取知识库所有分类"""
    # 合并数据库中已有的分类和内存中的分类
    db_categories = db.query(Knowledge.category).distinct().all()
    db_cats = set(c[0] for c in db_categories if c[0])
    all_categories = sorted(list(CATEGORIES | db_cats))
    return {"categories": all_categories}


@router.post("/categories", summary="添加分类")
async def add_category(
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """添加新分类（仅管理员）"""
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="分类名称不能为空")

    name = name.strip()
    if name in CATEGORIES:
        raise HTTPException(status_code=400, detail="分类已存在")

    CATEGORIES.add(name)
    return {"success": True, "message": f"分类 '{name}' 添加成功"}


@router.delete("/categories", summary="删除分类")
async def delete_category(
    name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """删除分类（仅管理员）"""
    if not name:
        raise HTTPException(status_code=400, detail="分类名称不能为空")

    # 检查是否有知识使用该分类
    count = db.query(Knowledge).filter(Knowledge.category == name).count()
    if count > 0:
        raise HTTPException(status_code=400, detail=f"该分类下还有 {count} 条知识，无法删除")

    if name in CATEGORIES:
        CATEGORIES.remove(name)
        return {"success": True, "message": f"分类 '{name}' 删除成功"}
    else:
        raise HTTPException(status_code=404, detail="分类不存在")


@router.get("/", response_model=List[KnowledgeResponse], summary="获取知识列表")
async def get_knowledges(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    review_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取知识库列表（仅显示已通过审核的，所有人可见）"""
    query = db.query(Knowledge)
    # 默认只返回已审核通过的知识
    if not review_status:
        query = query.filter(Knowledge.review_status == "approved")
    else:
        # 如果指定了review_status，则按指定的状态查询
        query = query.filter(Knowledge.review_status == review_status)
    if category:
        query = query.filter(Knowledge.category == category)
    knowledges = query.order_by(desc(Knowledge.created_at)).offset(skip).limit(limit).all()
    return knowledges


# 审核相关API - 必须在 /{knowledge_id} 之前定义
@router.get("/pending", response_model=List[KnowledgeResponse], summary="获取待审核列表")
async def get_pending_knowledges(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """获取所有待审核的知识（仅管理员）"""
    knowledges = db.query(Knowledge).filter(
        Knowledge.review_status == "pending"
    ).order_by(desc(Knowledge.created_at)).all()
    return knowledges


@router.get("/my-documents", response_model=List[KnowledgeResponse], summary="获取我的文档")
async def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户上传的所有文档"""
    user_id = current_user.id
    knowledges = db.query(Knowledge).filter(
        Knowledge.uploader_id == user_id
    ).order_by(desc(Knowledge.created_at)).all()
    return knowledges


@router.post("/{knowledge_id}/review", summary="审核知识")
async def review_knowledge(
    knowledge_id: int,
    review: ReviewAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """审核知识（仅管理员）"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )

    if knowledge.review_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该知识已审核"
        )

    if review.action == "approve":
        knowledge.review_status = "approved"
        knowledge.status = "completed"
        knowledge.reviewer_id = current_user.id
        knowledge.rejection_reason = None
    elif review.action == "reject":
        knowledge.review_status = "rejected"
        knowledge.status = "failed"
        knowledge.reviewer_id = current_user.id
        knowledge.rejection_reason = review.reason or "未提供拒绝原因"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的审核动作"
        )

    db.commit()
    db.refresh(knowledge)
    return {"message": f"审核{'通过' if review.action == 'approve' else '拒绝'}成功", "knowledge": knowledge}


@router.get("/{knowledge_id}", response_model=KnowledgeResponse, summary="获取知识详情")
async def get_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """获取知识详情"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )
    return knowledge


@router.get("/{knowledge_id}/download", summary="下载知识文件")
async def download_knowledge_file(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """下载知识关联的文件"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )

    if not knowledge.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该知识没有关联文件"
        )

    file_path = Path(knowledge.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    return FileResponse(
        path=str(file_path),
        filename=knowledge.file_name or file_path.name,
        media_type="application/octet-stream"
    )


@router.delete("/{knowledge_id}", summary="删除知识")
async def delete_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除知识"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )

    # 检查权限：只能删除自己上传的，或者管理员可以删除任意知识
    if (current_user.role != "admin" and
        knowledge.uploader_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除该知识"
        )

    # 删除关联的文件
    if knowledge.file_path:
        file_path = Path(knowledge.file_path)
        if file_path.exists():
            file_path.unlink()

    db.delete(knowledge)
    db.commit()
    return {"message": "删除成功"}
