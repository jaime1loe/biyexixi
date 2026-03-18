#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试成绩和课程评价API"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_grades_api():
    print("=== 测试成绩API ===")

    # 1. 登录
    print("\n1. 登录...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "testuser", "password": "123456"}
    )
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.status_code}")
        print(login_response.text)
        return

    token = login_response.json().get("access_token")
    print(f"登录成功，token: {token[:50]}...")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. 查询我的成绩
    print("\n2. 查询我的成绩...")
    grades_response = requests.get(
        f"{BASE_URL}/grades/student/my",
        headers=headers
    )
    print(f"状态码: {grades_response.status_code}")
    if grades_response.status_code == 200:
        grades = grades_response.json()
        print(f"成功获取 {len(grades)} 条成绩:")
        for grade in grades[:3]:
            print(f"  {grade['course_name']}: {grade['score']}分 ({grade['semester']})")
    else:
        print(f"失败: {grades_response.text}")

    # 3. 查询课程评价（测试是否需要先评价）
    print("\n3. 测试课程评价API...")
    eval_response = requests.get(
        f"{BASE_URL}/evaluations/my-evaluations",
        headers=headers
    )
    print(f"评价状态码: {eval_response.status_code}")
    if eval_response.status_code == 200:
        evals = eval_response.json()
        print(f"已有 {len(evals)} 条评价")
    else:
        print(f"评价查询失败: {eval_response.text}")

if __name__ == "__main__":
    test_grades_api()
