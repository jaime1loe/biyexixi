from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    real_name = Column(String(50), comment="真实姓名")
    student_id = Column(String(20), unique=True, comment="学号")
    email = Column(String(100), comment="邮箱")
    role = Column(String(20), default="student", comment="角色: student/teacher/admin")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    questions = relationship("Question", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class Question(Base):
    """问题表"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, comment="问题ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question = Column(Text, nullable=False, comment="问题内容")
    answer = Column(Text, comment="答案内容")
    category = Column(String(50), comment="问题分类")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关系
    user = relationship("User", back_populates="questions")
    feedbacks = relationship("Feedback", back_populates="question")


class Feedback(Base):
    """反馈评价表"""
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, comment="反馈ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="问题ID")
    rating = Column(Integer, nullable=False, comment="评分: 1-5星")
    comment = Column(Text, comment="评价内容")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关系
    user = relationship("User", back_populates="feedbacks")
    question = relationship("Question", back_populates="feedbacks")


class Knowledge(Base):
    """知识库表"""
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True, comment="知识ID")
    title = Column(String(200), nullable=False, comment="知识标题")
    content = Column(Text, nullable=False, comment="知识内容")
    category = Column(String(50), comment="分类")
    tags = Column(String(200), comment="标签，逗号分隔")
    file_path = Column(String(255), comment="关联文件路径")
    embedding = Column(Text, comment="向量数据(JSON)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class Statistics(Base):
    """统计表"""
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True, comment="统计ID")
    date = Column(String(10), unique=True, nullable=False, comment="日期")
    question_count = Column(Integer, default=0, comment="问题数")
    user_count = Column(Integer, default=0, comment="活跃用户数")
    avg_rating = Column(Float, default=0.0, comment="平均评分")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
