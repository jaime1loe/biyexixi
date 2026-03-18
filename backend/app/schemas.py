#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pydantic Schemas"""
from typing import Optional, Any, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ========== 用户相关 ==========
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
    bio: Optional[str] = None


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
    bio: Optional[str] = None


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


class ProfileChangeCreate(BaseModel):
    """个人信息修改申请创建"""
    real_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    reason: str = Field(..., description="修改原因")


class ProfileChangeResponse(BaseModel):
    """个人信息修改申请响应"""
    id: int
    user_id: int
    real_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    bio: Optional[str] = None
    reason: str
    status: str
    admin_comment: Optional[str] = None
    reviewed_by: Optional[int] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProfileChangeReview(BaseModel):
    """审核修改申请"""
    status: str = Field(..., description="审核状态: approved/rejected")
    admin_comment: Optional[str] = Field(None, description="审核意见")


class Token(BaseModel):
    """Token模型"""
    access_token: str
    token_type: str = "bearer"


# ========== 问答相关 ==========
class QuestionBase(BaseModel):
    """问题基础模型"""
    question: str = Field(..., min_length=1)
    category: Optional[str] = None
    answer: Optional[str] = None
    views: Optional[int] = 0
    ask_count: Optional[int] = 1
    is_public: Optional[int] = 1


class QuestionCreate(QuestionBase):
    """问题创建模型"""
    pass


class QuestionResponse(QuestionBase):
    """问题响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ========== 反馈相关 ==========
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
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 知识库相关 ==========
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
    uploader_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    review_status: Optional[str] = None
    rejection_reason: Optional[str] = None
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
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    tags: Optional[str] = None


# ========== 统计相关 ==========
class StatisticsResponse(BaseModel):
    """统计响应模型"""
    date: str
    question_count: int
    user_count: int
    avg_rating: float


class Result(BaseModel):
    """结果模型"""
    status: str = "success"
    message: str = "success"
    data: Optional[Any] = None


# ========== 收藏相关 ==========
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


# ========== 通知相关 ==========
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


class NotificationUpdate(BaseModel):
    """通知更新模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    detail_content: Optional[str] = None
    category: Optional[str] = None
    is_important: Optional[int] = None
    publisher: Optional[str] = None


class NotificationResponse(NotificationBase):
    """通知响应模型"""
    id: int
    file_path: Optional[str] = None
    views: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActivityLogResponse(BaseModel):
    """活动日志响应模型"""
    id: int
    user_id: int
    username: Optional[str] = None
    user_role: Optional[str] = None
    action_type: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    target_name: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewAction(BaseModel):
    """审核操作模型"""
    action: str = Field(..., description="审核动作: approve/reject")
    reason: Optional[str] = Field(None, description="拒绝原因（仅在拒绝时需要）")


# ========== 教室课程相关 ==========
class ClassroomCreate(BaseModel):
    """教室创建模型"""
    building: str = Field(..., description="教学楼")
    room_number: str = Field(..., description="教室号")
    capacity: int = Field(..., gt=0, description="容量")
    classroom_type: str = Field(..., description="教室类型")
    equipment: Optional[str] = Field(None, description="设备")


class ClassroomUpdate(BaseModel):
    """教室更新模型"""
    capacity: Optional[int] = Field(None, gt=0)
    classroom_type: Optional[str] = None
    equipment: Optional[str] = None
    status: Optional[str] = None


class ClassroomResponse(BaseModel):
    """教室响应模型"""
    id: int
    building: str
    room_number: str
    capacity: int
    classroom_type: str
    equipment: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    """课程创建模型"""
    course_code: str = Field(..., min_length=1, max_length=50)
    course_name: str = Field(..., min_length=1, max_length=200)
    credits: float = Field(..., gt=0)
    teacher_name: Optional[str] = None
    description: Optional[str] = None


class CourseUpdate(BaseModel):
    """课程更新模型"""
    course_code: Optional[str] = Field(None, min_length=1, max_length=50)
    course_name: Optional[str] = Field(None, min_length=1, max_length=200)
    credits: Optional[float] = Field(None, gt=0)
    teacher_name: Optional[str] = None
    description: Optional[str] = None


class CourseResponse(BaseModel):
    """课程响应模型"""
    id: int
    course_code: str
    course_name: str
    credits: float
    teacher_name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ScheduleCreate(BaseModel):
    """课表创建模型"""
    classroom_id: int
    course_id: int
    day_of_week: int = Field(..., ge=1, le=7)
    start_time: str
    end_time: str
    semester: str


class ScheduleUpdate(BaseModel):
    """课表更新模型"""
    classroom_id: Optional[int] = None
    course_id: Optional[int] = None
    day_of_week: Optional[int] = Field(None, ge=1, le=7)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    semester: Optional[str] = None


class ScheduleResponse(BaseModel):
    """课表响应模型"""
    id: int
    classroom_id: int
    course_id: int
    day_of_week: int
    start_time: str
    end_time: str
    semester: str
    classroom: Optional[ClassroomResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True


# ========== 成绩管理相关 ==========
class GradeCreate(BaseModel):
    """成绩创建模型"""
    student_id: int
    course_id: int
    semester: str
    score: float
    is_makeup: bool = False


class GradeUpdate(BaseModel):
    """成绩更新模型"""
    score: Optional[float] = None
    is_makeup: Optional[bool] = None


class GradeResponse(BaseModel):
    """成绩响应模型"""
    id: int
    student_id: int
    course_id: int
    semester: str
    score: float
    grade_point: Optional[float] = None
    grade_level: Optional[str] = None
    is_makeup: bool = False
    credits: Optional[float] = None
    course_name: Optional[str] = None
    course_code: Optional[str] = None

    class Config:
        from_attributes = True


class StudentGradeResponse(BaseModel):
    """学生成绩响应模型"""
    id: int
    student_id: int
    course_id: int
    semester: str
    score: float
    grade_point: Optional[float] = None
    grade_level: Optional[str] = None
    is_makeup: bool = False
    credits: Optional[float] = None
    gpa: Optional[float] = None
    course: Optional[dict] = None

    class Config:
        from_attributes = True


class GradeUpload(BaseModel):
    """成绩上传模型"""
    student_ids: list[int]
    course_id: int
    semester: str
    scores: list[float]


class Course(BaseModel):
    """课程模型"""
    id: int
    course_code: str
    course_name: str
    semester: str
    credits: float
    student_count: Optional[int] = None

    class Config:
        from_attributes = True


class StudentWithGrade(BaseModel):
    """带成绩的学生模型"""
    student_id: int
    student_name: str
    student_number: Optional[str] = None
    score: Optional[float] = None
    grade_level: Optional[str] = None
    is_makeup: bool = False
    grade_id: Optional[int] = None

    class Config:
        from_attributes = True


# ========== 课程评价相关 ==========
class CourseEvaluationCreate(BaseModel):
    """课程评价创建模型"""
    course_id: int = Field(..., description="课程ID")
    semester: str = Field(..., description="学期")
    teaching_quality: int = Field(..., ge=1, le=5, description="教学质量 1-5")
    course_content: int = Field(..., ge=1, le=5, description="课程内容 1-5")
    teacher_attitude: int = Field(..., ge=1, le=5, description="教师态度 1-5")
    difficulty: int = Field(..., ge=1, le=5, description="课程难度 1-5")
    workload: int = Field(..., ge=1, le=5, description="作业量 1-5")
    overall_rating: float = Field(..., ge=1, le=5, description="总体评分 1-5")
    comment: Optional[str] = Field(None, description="评价内容")
    is_recommended: int = Field(0, ge=0, le=1, description="是否推荐")


class CourseEvaluationUpdate(BaseModel):
    """课程评价更新模型"""
    teaching_quality: Optional[int] = Field(None, ge=1, le=5)
    course_content: Optional[int] = Field(None, ge=1, le=5)
    teacher_attitude: Optional[int] = Field(None, ge=1, le=5)
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    workload: Optional[int] = Field(None, ge=1, le=5)
    overall_rating: Optional[float] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    is_recommended: Optional[int] = Field(None, ge=0, le=1)


class CourseEvaluationResponse(BaseModel):
    """课程评价响应模型"""
    id: int
    student_id: int
    student_name: Optional[str] = None
    course_id: int
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    teacher_id: int
    teacher_name: Optional[str] = None
    semester: str
    teaching_quality: int
    course_content: int
    teacher_attitude: int
    difficulty: int
    workload: int
    overall_rating: float
    comment: Optional[str] = None
    is_recommended: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourseEvaluationStats(BaseModel):
    """课程评价统计模型"""
    course_id: int
    course_name: str
    teacher_name: str
    semester: str
    total_evaluations: int
    average_ratings: dict
    recommendation_rate: float
