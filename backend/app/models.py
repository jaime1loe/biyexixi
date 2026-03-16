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
    phone = Column(String(20), comment="电话")
    avatar = Column(String(255), comment="头像路径")
    role = Column(String(20), default="student", comment="角色: student/teacher/admin")
    department = Column(String(50), comment="院系")
    major = Column(String(50), comment="专业")
    class_name = Column(String(50), comment="班级")
    bio = Column(Text, comment="个人简介")
    is_active = Column(Integer, default=1, comment="是否激活: 1=激活, 0=禁用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    questions = relationship("Question", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    profile_changes = relationship("ProfileChangeRequest", foreign_keys="ProfileChangeRequest.user_id", back_populates="user")
    reviewed_changes = relationship("ProfileChangeRequest", foreign_keys="ProfileChangeRequest.reviewed_by", back_populates="reviewer")


class ProfileChangeRequest(Base):
    """个人信息修改申请表"""
    __tablename__ = "profile_change_requests"

    id = Column(Integer, primary_key=True, index=True, comment="申请ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    real_name = Column(String(50), comment="真实姓名")
    email = Column(String(100), comment="邮箱")
    phone = Column(String(20), comment="电话")
    department = Column(String(50), comment="院系")
    major = Column(String(50), comment="专业")
    bio = Column(Text, comment="个人简介")
    reason = Column(Text, comment="修改原因")
    status = Column(String(20), default="pending", comment="状态: pending/approved/rejected")
    admin_comment = Column(Text, comment="管理员审核意见")
    reviewed_by = Column(Integer, ForeignKey("users.id"), comment="审核管理员ID")
    created_at = Column(DateTime, default=datetime.now, comment="申请时间")
    reviewed_at = Column(DateTime, comment="审核时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id], back_populates="profile_changes")
    reviewer = relationship("User", foreign_keys=[reviewed_by], back_populates="reviewed_changes")


class Question(Base):
    """问题表"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, comment="问题ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question = Column(Text, nullable=False, comment="问题内容")
    answer = Column(Text, comment="答案内容")
    category = Column(String(50), comment="问题分类")
    views = Column(Integer, default=0, comment="浏览次数")
    ask_count = Column(Integer, default=1, comment="提问次数")
    is_public = Column(Integer, default=1, comment="是否公开: 1=公开, 0=私密")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

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
    status = Column(String(20), default="pending", comment="状态: pending=待处理, processing=处理中, completed=已完成, failed=失败")
    # 审核相关字段
    uploader_id = Column(Integer, ForeignKey("users.id"), comment="上传者用户ID")
    reviewer_id = Column(Integer, ForeignKey("users.id"), comment="审核人用户ID")
    review_status = Column(String(20), default="pending", comment="审核状态: pending=待审核, approved=已通过, rejected=已拒绝")
    rejection_reason = Column(Text, comment="拒绝原因")
    # 文件相关字段
    file_name = Column(String(255), comment="文件名")
    file_path = Column(String(255), comment="文件存储路径")
    file_type = Column(String(50), comment="文件类型")
    file_size = Column(Integer, comment="文件大小(字节)")
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


class Favorite(Base):
    """收藏表"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, comment="收藏ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="问题ID")
    created_at = Column(DateTime, default=datetime.now, comment="收藏时间")


class Notification(Base):
    """通知表"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, comment="通知ID")
    title = Column(String(200), nullable=False, comment="通知标题")
    content = Column(Text, comment="通知内容（摘要）")
    detail_content = Column(Text, comment="详细内容")
    category = Column(String(50), comment="通知分类")
    is_important = Column(Integer, default=0, comment="是否重要: 1=重要, 0=普通")
    file_path = Column(String(255), comment="附件路径")
    publisher = Column(String(100), comment="发布单位")
    views = Column(Integer, default=0, comment="浏览次数")
    created_at = Column(DateTime, default=datetime.now, comment="发布时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
