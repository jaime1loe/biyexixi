#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
后端服务启动脚本
"""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import uvicorn
from app.config import settings

print("=" * 60)
print(f"启动 {settings.APP_NAME}")
print("=" * 60)
print(f"版本: {settings.APP_VERSION}")
print(f"调试模式: {settings.DEBUG}")
print(f"主机: {settings.HOST}")
print(f"端口: {settings.PORT}")
print(f"数据库: {settings.DB_NAME}")
print("=" * 60)
print("\n服务启动中...")
print("按 Ctrl+C 停止服务\n")

uvicorn.run(
    "main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=settings.DEBUG
)
