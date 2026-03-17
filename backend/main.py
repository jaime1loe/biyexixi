import sys
import os
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 现在使用相对导入
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

# 使用相对导入避免路径问题
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, questions, knowledge, feedback, statistics, users, favorites, notifications, campus, profile_changes
from app.exceptions import (
    sqlalchemy_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="基于大模型智能体的高校知识库在线答疑系统API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)


# 定时任务：发布定时到期的通知
def publish_scheduled_task():
    """定时任务：发布到期的通知"""
    db = SessionLocal()
    try:
        now = datetime.now()
        from app.models import Notification

        scheduled_notifications = db.query(Notification).filter(
            Notification.status == "scheduled",
            Notification.schedule_time <= now
        ).all()

        for notification in scheduled_notifications:
            notification.status = "published"
            notification.published_at = now

        if scheduled_notifications:
            db.commit()
            print(f"[{datetime.now()}] 已发布 {len(scheduled_notifications)} 条定时通知")
    except Exception as e:
        print(f"[{datetime.now()}] 发布定时通知失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


# 创建定时任务调度器
scheduler = BackgroundScheduler()


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化定时任务"""
    # 每分钟检查一次待发布的定时通知
    scheduler.add_job(
        publish_scheduled_task,
        'interval',
        minutes=1,
        id='publish_scheduled_notifications'
    )
    scheduler.start()
    print("[启动] 定时任务调度器已启动")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时停止定时任务"""
    scheduler.shutdown()
    print("[关闭] 定时任务调度器已停止")


# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(questions.router, prefix="/api/questions", tags=["问答"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["反馈"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["收藏"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["通知"])
app.include_router(campus.router, prefix="/api/campus", tags=["校园服务"])
app.include_router(profile_changes.router, tags=["信息修改"])


@app.get("/", summary="健康检查")
async def root():
    """根路径接口"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", summary="健康检查")
async def health():
    """健康检查接口"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
