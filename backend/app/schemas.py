from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[EmailStr] = None
    role: str = "student"


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """用户更新模型"""
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


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
    answer: Optional[str] = None
    created_at: datetime
    user: UserResponse

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
    rating: int
    comment: Optional[str]
    created_at: datetime
    user: UserResponse
    question: QuestionResponse

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
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
    data: Optional[any] = None
