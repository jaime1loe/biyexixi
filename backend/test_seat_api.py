#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试座位API"""
import requests

BASE_URL = "http://127.0.0.1:8000"

# 先登录获取token
try:
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "testuser",
        "password": "123456"
    })
    print(f"登录响应: {login_response.status_code}")
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"Token获取成功")

        # 测试座位API
        response = requests.get(f"{BASE_URL}/api/campus/library/seats", headers=headers)
        print(f"\nGET /api/campus/library/seats: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total: {data.get('total', 0)}")
            print(f"  Available: {data.get('available', 0)}")
            print(f"  Occupied: {data.get('occupied', 0)}")
            print(f"  Reserved: {data.get('reserved', 0)}")
            seats = data.get('seats', [])
            if seats:
                print(f"  First seat: {seats[0]}")
        else:
            print(f"  Error: {response.text}")

        # 测试楼层
        response = requests.get(f"{BASE_URL}/api/campus/library/floors", headers=headers)
        print(f"\nGET /api/campus/library/floors: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Floors: {data}")
        else:
            print(f"  Error: {response.text}")

        # 测试区域
        response = requests.get(f"{BASE_URL}/api/campus/library/areas", headers=headers)
        print(f"\nGET /api/campus/library/areas: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Areas: {data}")
        else:
            print(f"  Error: {response.text}")
    else:
        print(f"登录失败: {login_response.text}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
