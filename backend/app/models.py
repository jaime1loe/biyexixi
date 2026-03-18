from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
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
    activities = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="teacher")
    grades_as_student = relationship("Grade", foreign_keys="Grade.student_id", back_populates="student", cascade="all, delete-orphan")
    grades_as_teacher = relationship("Grade", foreign_keys="Grade.teacher_id", back_populates="teacher", cascade="all, delete-orphan")


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
    # 定时发布字段
    schedule_time = Column(DateTime, comment="定时发布时间")
    status = Column(String(20), default="published", comment="状态: published=已发布, scheduled=待定时, draft=草稿")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    published_at = Column(DateTime, comment="实际发布时间")


class ActivityLog(Base):
    """活动记录表"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True, comment="活动ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    action_type = Column(String(50), nullable=False, comment="操作类型")
    target_type = Column(String(50), comment="目标类型")
    target_id = Column(Integer, comment="目标ID")
    target_name = Column(String(200), comment="目标名称")
    details = Column(Text, comment="详细信息")
    ip_address = Column(String(50), comment="IP地址")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关系
    user = relationship("User", back_populates="activities")


class Classroom(Base):
    """教室表"""
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True, comment="教室ID")
    building = Column(String(50), nullable=False, comment="教学楼：教一到教十一")
    room_number = Column(String(50), nullable=False, comment="教室号")
    capacity = Column(Integer, default=40, comment="教室容量")
    room_type = Column(String(20), default="普通", comment="教室类型：普通/多媒体/实验室")
    equipment = Column(String(200), comment="设备：投影仪、音响等")
    floor = Column(Integer, comment="楼层")
    is_available = Column(Integer, default=1, comment="是否可用：1=可用, 0=不可用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    schedules = relationship("Schedule", back_populates="classroom", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Classroom {self.building}{self.room_number}>"


class Course(Base):
    """课程表"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, comment="课程ID")
    course_code = Column(String(50), unique=True, nullable=False, comment="课程代码")
    course_name = Column(String(100), nullable=False, comment="课程名称")
    teacher_id = Column(Integer, ForeignKey("users.id"), comment="授课教师ID")
    teacher_name = Column(String(50), comment="授课教师")
    department = Column(String(50), comment="开课院系")
    credits = Column(Float, comment="学分")
    hours = Column(Integer, comment="学时")
    course_type = Column(String(20), default="必修", comment="课程类型：必修/选修/实践")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    schedules = relationship("Schedule", back_populates="course", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")
    evaluations = relationship("CourseEvaluation", back_populates="course", cascade="all, delete-orphan")
    teacher = relationship("User", back_populates="courses")

    def __repr__(self):
        return f"<Course {self.course_code} - {self.course_name}>"


class Schedule(Base):
    """排课表"""
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True, comment="排课ID")
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False, comment="教室ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")
    day_of_week = Column(Integer, nullable=False, comment="星期：1-7（1=周一）")
    period = Column(Integer, nullable=False, comment="节次：1-5")
    week_start = Column(Integer, default=1, comment="起始周")
    week_end = Column(Integer, default=18, comment="结束周")
    semester = Column(String(20), nullable=False, comment="学期：2024-2025-1")
    class_name = Column(String(50), comment="班级名称")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    classroom = relationship("Classroom", back_populates="schedules")
    course = relationship("Course", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule {self.day_of_week}-{self.period} {self.classroom.building}{self.classroom.room_number}>"


class Grade(Base):
    """成绩表"""
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True, comment="成绩ID")
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="学生ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True, comment="课程ID")
    semester = Column(String(20), index=True, comment="学期")
    score = Column(Float, comment="成绩")
    grade_point = Column(Float, comment="绩点")
    grade_level = Column(String(10), comment="等级：A/B/C/D/F")
    is_makeup = Column(Boolean, default=False, comment="是否补考")
    makeup_score = Column(Float, nullable=True, comment="补考成绩")
    teacher_id = Column(Integer, ForeignKey("users.id"), comment="录入教师ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    student = relationship("User", foreign_keys=[student_id], back_populates="grades_as_student")
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="grades_as_teacher")
    course = relationship("Course", back_populates="grades")

    def __repr__(self):
        return f"<Grade student_id={self.student_id}, course_id={self.course_id}, score={self.score}>"


class Book(Base):
    """图书表"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, comment="图书ID")
    title = Column(String(200), nullable=False, comment="书名")
    author = Column(String(100), comment="作者")
    publisher = Column(String(100), comment="出版社")
    publish_year = Column(Integer, comment="出版年份")
    isbn = Column(String(20), comment="ISBN")
    category = Column(String(50), comment="分类")
    location = Column(String(50), comment="馆藏位置")
    total_copies = Column(Integer, default=1, comment="总复本数")
    available_copies = Column(Integer, default=1, comment="可借复本数")
    status = Column(String(20), default="可借", comment="状态：可借/借出/预约/维护")
    language = Column(String(20), comment="语言：中文/英文等")
    pages = Column(Integer, comment="页数")
    price = Column(Float, comment="价格")
    description = Column(Text, comment="简介")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<Book {self.title} - {self.author}>"


class Seat(Base):
    """图书馆座位表"""
    __tablename__ = "library_seats"

    id = Column(Integer, primary_key=True, index=True, comment="座位ID")
    seat_number = Column(String(20), nullable=False, comment="座位号")
    floor = Column(Integer, nullable=False, comment="楼层")
    area = Column(String(50), comment="区域：阅览区/自习区/研讨区等")
    seat_type = Column(String(20), default="普通", comment="座位类型：普通/靠窗/安静区/电源位")
    status = Column(String(20), default="available", comment="状态：available=空闲, occupied=有人, reserved=已预约")
    is_available = Column(Integer, default=1, comment="是否可用：1=可用, 0=不可用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    reservations = relationship("SeatReservation", back_populates="seat", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Seat {self.seat_number} - {self.area}>"


class SeatReservation(Base):
    """座位预约表"""
    __tablename__ = "seat_reservations"

    id = Column(Integer, primary_key=True, index=True, comment="预约ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    seat_id = Column(Integer, ForeignKey("library_seats.id"), nullable=False, comment="座位ID")
    reservation_date = Column(String(10), nullable=False, comment="预约日期：YYYY-MM-DD")
    start_time = Column(String(5), comment="开始时间：HH:MM")
    end_time = Column(String(5), comment="结束时间：HH:MM")
    status = Column(String(20), default="reserved", comment="状态：reserved=已预约, checked_in=已签到, cancelled=已取消")
    check_in_time = Column(DateTime, comment="签到时间")
    check_out_time = Column(DateTime, comment="签退时间")
    created_at = Column(DateTime, default=datetime.now, comment="预约时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    user = relationship("User")
    seat = relationship("Seat", back_populates="reservations")

    def __repr__(self):
        return f"<SeatReservation user_id={self.user_id}, seat_id={self.seat_id}>"


class CourseEvaluation(Base):
    """课程评价表"""
    __tablename__ = "course_evaluations"

    id = Column(Integer, primary_key=True, index=True, comment="评价ID")
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学生ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="教师ID")
    semester = Column(String(20), nullable=False, comment="学期：2024-2025-1")

    # 评价维度（1-5分）
    teaching_quality = Column(Integer, comment="教学质量 1-5")
    course_content = Column(Integer, comment="课程内容 1-5")
    teacher_attitude = Column(Integer, comment="教师态度 1-5")
    difficulty = Column(Integer, comment="课程难度 1-5")
    workload = Column(Integer, comment="作业量 1-5")

    # 总体评分（1-5分）
    overall_rating = Column(Float, comment="总体评分 1-5")

    # 文字评价
    comment = Column(Text, comment="评价内容")

    # 推荐
    is_recommended = Column(Integer, default=0, comment="是否推荐：1=推荐, 0=不推荐")

    created_at = Column(DateTime, default=datetime.now, comment="评价时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    student = relationship("User", foreign_keys=[student_id])
    teacher = relationship("User", foreign_keys=[teacher_id])
    course = relationship("Course", back_populates="evaluations")

    def __repr__(self):
        return f"<CourseEvaluation student_id={self.student_id}, course_id={self.course_id}, rating={self.overall_rating}>"
