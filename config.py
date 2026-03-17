"""
AI服务配置文件 - 校园智能问答系统
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """应用配置"""

    # 应用基本信息
    APP_NAME: str = "校园智能问答AI服务"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    # Ollama配置
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2:7b"
    OLLAMA_TIMEOUT: int = 120

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = str(BASE_DIR / "logs" / "ai_service.log")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 确保日志目录存在
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
