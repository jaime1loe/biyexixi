#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查路由定义"""
from app.routers import notifications

routes = notifications.router.routes
print("路由列表:")
for r in routes:
    if 'GET' in r.methods or 'POST' in r.methods:
        print(f"  {r.methods} {r.path}")
