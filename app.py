"""
FastAPI主应用 - AI问答服务
提供智能问答接口给主系统调用
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from config import settings
from simple_model_client import simple_llm_client

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="校园智能问答AI服务"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Pydantic模型 ==========

class QARequest(BaseModel):
    """问答请求"""
    question: str
    guided: bool = False
    history: Optional[List[dict]] = []
    regenerate: Optional[bool] = False


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求"""
    messages: List[ChatMessage]
    temperature: float = 0.7


# ========== 路由 ==========

@app.get("/", summary="根路径")
async def root():
    """根路径"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查"""
    model_status = simple_llm_client.health_check()
    return {
        "status": "healthy",
        "model": model_status["model"],
        "knowledge_items": model_status["knowledge_items"]
    }


@app.post("/api/qa", summary="智能问答")
async def qa(request: QARequest):
    """
    智能问答接口

    - question: 用户问题
    - guided: 是否为引导式学习模式
    """
    try:
        logger.info(f"收到问答请求: {request.question}, 引导模式: {request.guided}")

        # 使用简化模型客户端回答问题（包含历史对话）
        result = await simple_llm_client.generate(
            request.question,
            history=request.history if request.history else []
        )

        # 返回结果
        return {
            "question": request.question,
            "answer": result.answer,
            "suggested_questions": result.suggested_questions,
            "sources": [],
            "success": True,
            "guided": request.guided
        }
    except Exception as e:
        logger.error(f"问答失败: {e}")
        return {
            "question": request.question,
            "answer": f"系统错误: {str(e)}",
            "suggested_questions": [],
            "sources": [],
            "success": False,
            "guided": request.guided
        }


@app.post("/api/chat", summary="普通聊天")
async def chat(request: ChatRequest):
    """普通聊天接口"""
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="消息列表为空")

        last_message = request.messages[-1]
        if last_message.role != "user":
            raise HTTPException(status_code=400, detail="最后一条消息不是用户消息")

        response = await simple_llm_client.generate(
            last_message.content,
            temperature=request.temperature,
            max_tokens=500
        )

        return {
            "response": response
        }
    except Exception as e:
        logger.error(f"聊天失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
