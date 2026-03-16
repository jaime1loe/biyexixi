"""添加示例数据"""
from app.database import SessionLocal, Base, engine
from app.models import Notification, Question
from datetime import datetime

# 创建数据库会话
db = SessionLocal()

try:
    # 添加示例通知
    print("添加示例通知...")
    notifications = [
        Notification(
            title="系统维护通知",
            content="系统将于本周六凌晨2:00-4:00进行维护升级，届时将无法正常使用，请提前做好准备。",
            category="系统公告",
            is_important=1,
            created_at=datetime.now()
        ),
        Notification(
            title="新功能上线通知",
            content="知识库智能问答功能已上线，欢迎体验！如有问题请及时反馈。",
            category="功能更新",
            is_important=0,
            created_at=datetime.now()
        ),
        Notification(
            title="校园服务功能优化",
            content="校园服务模块已完成优化，空教室查询、成绩查询等功能更加便捷。",
            category="功能更新",
            is_important=0,
            created_at=datetime.now()
        )
    ]

    for notification in notifications:
        db.add(notification)

    db.commit()
    print(f"成功添加 {len(notifications)} 条通知")

    # 查看现有问题数据
    print("\n现有问题数据：")
    questions = db.query(Question).all()
    for q in questions:
        print(f"- ID: {q.id}, 问题: {q.question[:50]}...")

except Exception as e:
    print(f"错误: {e}")
    db.rollback()
finally:
    db.close()

print("\n示例数据添加完成!")
