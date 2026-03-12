#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试异常处理器
"""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("测试异常处理器...")

try:
    from app.exceptions import (
        sqlalchemy_exception_handler,
        http_exception_handler,
        validation_exception_handler
    )
    print("[OK] 异常处理器导入成功")

    from main import app
    print("[OK] FastAPI应用加载成功")
    print(f"    应用名称: {app.title}")
    print(f"    路由数量: {len(app.routes)}")

    print("\n[OK] 所有测试通过！")
except Exception as e:
    print(f"[FAIL] 测试失败: {e}")
    import traceback
    traceback.print_exc()
