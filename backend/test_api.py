#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试通知API"""
import requests

BASE_URL = "http://127.0.0.1:8000"

# 测试GET /api/notifications
try:
    response = requests.get(f"{BASE_URL}/api/notifications?include_scheduled=true")
    print(f"GET /api/notifications:")
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Count: {len(data)}")
        if data:
            print(f"  First notification: {data[0]['title']}")
    else:
        print(f"  Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
