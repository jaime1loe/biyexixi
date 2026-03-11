from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
import shutil
from pathlib import Path
import json

from app.database import get_db
from app.models import Knowledge
from app.schemas import KnowledgeCreate, KnowledgeResponse
from app.dependencies import get_current_admin_user, get_current_user
from app.config import settings

router = APIRouter()

# 确保上传目录存在
UPLOAD_DIR = Path("uploads/knowledge")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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
    title: str,
    content: str,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """上传文件并添加知识（仅管理员）"""
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

    db_knowledge = Knowledge(
        title=title,
        content=content,
        category=category,
        tags=tags,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)

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
    categories = db.query(Knowledge.category).distinct().all()
    return {"categories": [c[0] for c in categories if c[0]]}


@router.get("/", response_model=List[KnowledgeResponse], summary="获取知识列表")
async def get_knowledges(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取知识库列表"""
    query = db.query(Knowledge)
    if category:
        query = query.filter(Knowledge.category == category)
    knowledges = query.order_by(desc(Knowledge.created_at)).offset(skip).limit(limit).all()
    return knowledges


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
    current_user = Depends(get_current_admin_user)
):
    """删除知识（仅管理员）"""
    knowledge = db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识不存在"
        )
    
    # 删除关联的文件
    if knowledge.file_path:
        file_path = Path(knowledge.file_path)
        if file_path.exists():
            file_path.unlink()
    
    db.delete(knowledge)
    db.commit()
    return {"message": "删除成功"}
