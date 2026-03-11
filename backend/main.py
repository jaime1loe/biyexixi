import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.routers import auth, questions, knowledge, feedback, statistics, users, favorites, notifications, campus
from backend.app.exceptions import (
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


@app.get("/", summary="健康检查")
async def root():
    """根路径接口"""
    return {
        "app": config.settings.APP_NAME,
        "version": config.settings.APP_VERSION,
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
