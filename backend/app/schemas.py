from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    role: str = "student"
    department: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """用户更新模型"""
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str


class Token(BaseModel):
    """Token模型"""
    access_token: str
    token_type: str = "bearer"


class QuestionBase(BaseModel):
    """问题基础模型"""
    question: str = Field(..., min_length=1)
    category: Optional[str] = None


class QuestionCreate(QuestionBase):
    """问题创建模型"""
    pass


class QuestionResponse(QuestionBase):
    """问题响应模型"""
    id: int
    user_id: int
    answer: Optional[str] = None
    category: Optional[str] = None
    views: Optional[int] = 0
    ask_count: Optional[int] = 1
    is_public: Optional[int] = 1
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    """反馈创建模型"""
    question_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    """反馈响应模型"""
    id: int
    user_id: int
    question_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class KnowledgeBase(BaseModel):
    """知识基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: Optional[str] = None
    tags: Optional[str] = None


class KnowledgeCreate(KnowledgeBase):
    """知识创建模型"""
    pass


class KnowledgeResponse(KnowledgeBase):
    """知识响应模型"""
    id: int
    status: Optional[str] = None
    # 审核相关字段
    uploader_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    review_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    # 文件相关字段
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    embedding: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeUpdate(BaseModel):
    """知识更新模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None


class StatisticsResponse(BaseModel):
    """统计响应模型"""
    date: str
    question_count: int
    user_count: int
    avg_rating: float


class Result(BaseModel):
    """统一响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


class FavoriteCreate(BaseModel):
    """收藏创建模型"""
    question_id: int


class FavoriteResponse(BaseModel):
    """收藏响应模型"""
    id: int
    user_id: int
    question_id: int
    created_at: datetime
    question: Optional[str] = None
    answer: Optional[str] = None

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    """通知基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    detail_content: Optional[str] = None
    category: Optional[str] = None
    is_important: int = 0
    publisher: Optional[str] = None


class NotificationCreate(NotificationBase):
    """通知创建模型"""
    pass


class NotificationResponse(NotificationBase):
    """通知响应模型"""
    id: int
    file_path: Optional[str] = None
    views: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewAction(BaseModel):
    """审核操作模型"""
    action: str = Field(..., description="审核动作: approve/reject")
    reason: Optional[str] = Field(None, description="拒绝原因（仅在拒绝时需要）")
