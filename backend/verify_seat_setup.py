# -*- coding: utf-8 -*-
"""验证座位功能完整设置"""
import sys
import requests

sys.path.insert(0, r'd:\毕业设计\backend')

from app.database import SessionLocal
from app.models import Seat, SeatReservation

print("=" * 60)
print("验证图书馆座位功能设置")
print("=" * 60)

# 1. 检查数据库中的座位数据
print("\n1. 检查座位数据...")
db = SessionLocal()
try:
    total_seats = db.query(Seat).count()
    available_seats = db.query(Seat).filter(Seat.status == "available").count()
    occupied_seats = db.query(Seat).filter(Seat.status == "occupied").count()
    reserved_seats = db.query(Seat).filter(Seat.status == "reserved").count()

    print(f"[OK] 总座位数: {total_seats}")
    print(f"[OK] 空闲: {available_seats}")
    print(f"[OK] 有人: {occupied_seats}")
    print(f"[OK] 已预约: {reserved_seats}")

    # 显示各楼层座位分布
    print("\n2. 座位楼层分布:")
    for floor in [1, 2, 3, 4]:
        floor_seats = db.query(Seat).filter(Seat.floor == floor).count()
        print(f"  {floor}楼: {floor_seats} 个座位")

    # 显示各区域座位分布
    print("\n3. 座位区域分布:")
    areas = db.query(Seat.area).distinct().all()
    for (area,) in sorted(areas):
        area_seats = db.query(Seat).filter(Seat.area == area).count()
        print(f"  {area}: {area_seats} 个座位")

finally:
    db.close()

# 2. 测试API接口
print("\n4. 测试API接口...")
base_url = "http://localhost:8000/api"

# 登录
print("\n  4.1 登录...")
try:
    login_response = requests.post(f"{base_url}/auth/login", json={
        "username": "testuser",
        "password": "123456"
    })

    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        print(f"  [OK] 登录成功")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 测试获取楼层
        print("  4.2 测试获取楼层...")
        floors_response = requests.get(f"{base_url}/campus/library/floors", headers=headers)
        if floors_response.status_code == 200:
            floors = floors_response.json()
            print(f"  [OK] 获取楼层成功: {floors['floors']}")
        else:
            print(f"  [ERROR] 获取楼层失败: {floors_response.status_code}")

        # 测试获取区域
        print("  4.3 测试获取区域...")
        areas_response = requests.get(f"{base_url}/campus/library/areas", headers=headers)
        if areas_response.status_code == 200:
            areas = areas_response.json()
            print(f"  [OK] 获取区域成功: {areas['areas']}")
        else:
            print(f"  [ERROR] 获取区域失败: {areas_response.status_code}")

        # 测试获取座位
        print("  4.4 测试获取座位...")
        seats_response = requests.get(f"{base_url}/campus/library/seats", headers=headers)
        if seats_response.status_code == 200:
            seats_data = seats_response.json()
            print(f"  [OK] 获取座位成功:")
            print(f"    总数: {seats_data['total']}")
            print(f"    空闲: {seats_data['available']}")
            print(f"    已预约: {seats_data['reserved']}")
            print(f"    有人: {seats_data['occupied']}")
        else:
            print(f"  [ERROR] 获取座位失败: {seats_response.status_code}")

        # 测试按楼层筛选
        print("  4.5 测试按楼层筛选...")
        filtered_response = requests.get(
            f"{base_url}/campus/library/seats?floor=2",
            headers=headers
        )
        if filtered_response.status_code == 200:
            filtered_data = filtered_response.json()
            print(f"  [OK] 按楼层筛选成功: 2楼有 {filtered_data['total']} 个座位")
        else:
            print(f"  [ERROR] 按楼层筛选失败: {filtered_response.status_code}")

    else:
        print(f"  [ERROR] 登录失败: {login_response.status_code}")
        print(f"    错误信息: {login_response.text}")

except requests.exceptions.ConnectionError:
    print("  [ERROR] 无法连接到后端服务")
    print("    请确保后端服务正在运行:")
    print("    cd d:/毕业设计/backend && python main.py")
except Exception as e:
    print(f"  [ERROR] 测试出错: {str(e)}")

print("\n" + "=" * 60)
print("验证完成！")
print("=" * 60)
