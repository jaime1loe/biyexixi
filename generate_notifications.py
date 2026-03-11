#!/usr/bin/env python3
"""
生成示例通知数据的脚本
"""
import sys
import os
from datetime import datetime, timedelta

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.database import SessionLocal
    from app.models import Notification
    
    print("正在生成示例通知数据...")
    
    # 示例通知数据
    sample_notifications = [
        {
            "title": "系统升级维护通知",
            "content": "为了提升系统性能，将于本周五晚上10点至周六凌晨2点进行系统维护升级，期间系统将暂停服务。",
            "category": "系统公告",
            "is_important": 1
        },
        {
            "title": "新学期课程安排",
            "content": "新学期课程安排已发布，请各位同学及时登录系统查看自己的课程表。",
            "category": "教务通知",
            "is_important": 0
        },
        {
            "title": "图书馆开放时间调整",
            "content": "由于期末考试临近，图书馆将延长开放时间至晚上11点，欢迎同学们前来学习。",
            "category": "校园生活",
            "is_important": 0
        },
        {
            "title": "重要安全提醒",
            "content": "近期发现有不法分子冒充学校工作人员进行诈骗，请同学们提高警惕，不要轻信陌生电话。",
            "category": "安全提醒",
            "is_important": 1
        },
        {
            "title": "奖学金评选通知",
            "content": "2025年度奖学金评选工作已开始，请符合条件的同学在规定时间内提交申请材料。",
            "category": "奖学金",
            "is_important": 0
        }
    ]
    
    db = SessionLocal()
    try:
        # 检查是否已有通知数据
        existing_count = db.query(Notification).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 条通知数据")
        else:
            # 插入示例数据
            for i, notification_data in enumerate(sample_notifications):
                # 设置不同的创建时间
                created_at = datetime.now() - timedelta(days=i*2)
                
                notification = Notification(
                    title=notification_data["title"],
                    content=notification_data["content"],
                    category=notification_data["category"],
                    is_important=notification_data["is_important"],
                    created_at=created_at
                )
                db.add(notification)
            
            db.commit()
            print(f"成功插入 {len(sample_notifications)} 条示例通知数据")
        
        # 显示通知数据
        notifications = db.query(Notification).order_by(Notification.created_at.desc()).all()
        print(f"\n当前通知列表（共 {len(notifications)} 条）:")
        for notif in notifications:
            importance = "重要" if notif.is_important == 1 else "普通"
            print(f"- [{notif.category}] {notif.title} ({importance})")
            
    finally:
        db.close()
    
    print("\n通知数据生成完成！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()