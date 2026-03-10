"""
初始化测试数据脚本
运行此脚本可以创建初始管理员用户和测试数据
"""

from app.database import SessionLocal, engine
from app.models import User, Question, Feedback, Knowledge
from app.utils import get_password_hash
from datetime import datetime


def init_data():
    """初始化测试数据"""
    db = SessionLocal()
    
    try:
        # 创建管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                real_name="系统管理员",
                role="admin",
                email="admin@university.edu"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✓ 创建管理员用户: admin / admin123")
        
        # 创建测试教师用户
        teacher = db.query(User).filter(User.username == "teacher").first()
        if not teacher:
            teacher = User(
                username="teacher",
                password_hash=get_password_hash("teacher123"),
                real_name="王老师",
                student_id=None,
                role="teacher",
                email="teacher@university.edu"
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print("✓ 创建教师用户: teacher / teacher123")
        
        # 创建测试学生用户
        students_data = [
            {"username": "student1", "real_name": "张三", "student_id": "20240001"},
            {"username": "student2", "real_name": "李四", "student_id": "20240002"},
            {"username": "student3", "real_name": "王五", "student_id": "20240003"},
        ]
        
        for data in students_data:
            student = db.query(User).filter(User.username == data["username"]).first()
            if not student:
                student = User(
                    username=data["username"],
                    password_hash=get_password_hash("student123"),
                    real_name=data["real_name"],
                    student_id=data["student_id"],
                    role="student",
                    email=f"{data['username']}@university.edu"
                )
                db.add(student)
                db.commit()
                db.refresh(student)
                print(f"✓ 创建学生用户: {data['username']} / student123")
        
        # 创建知识库数据
        knowledge_data = [
            {
                "title": "大学计算机基础",
                "content": "大学计算机基础课程主要介绍计算机的基本概念、原理和应用。包括计算机组成原理、操作系统、办公软件使用等内容。学习本课程需要掌握基本的计算机操作技能。",
                "category": "计算机",
                "tags": "基础,入门,必修"
            },
            {
                "title": "高等数学微积分",
                "content": "微积分是高等数学的核心内容，主要研究函数的极限、导数、微分和积分。微积分在物理、工程、经济等领域有广泛应用。学习重点是理解极限思想和掌握基本计算方法。",
                "category": "数学",
                "tags": "微积分,高等数学,必修"
            },
            {
                "title": "大学英语四级考试",
                "content": "大学英语四级考试是全国统一考试，主要测试学生的英语综合能力。考试内容包括听力、阅读、写作和翻译。建议学生提前三个月开始准备，每天坚持练习。",
                "category": "英语",
                "tags": "四级,英语,考试"
            },
            {
                "title": "数据结构课程介绍",
                "content": "数据结构是计算机专业核心课程，主要研究数据的组织方式和操作算法。包括线性表、栈、队列、树、图等基本数据结构。学好数据结构对编程能力提升有很大帮助。",
                "category": "计算机",
                "tags": "数据结构,算法,必修"
            },
            {
                "title": "线性代数基础",
                "content": "线性代数是现代数学的重要分支，主要研究向量空间和线性变换。内容包括行列式、矩阵、向量、线性方程组等。线性代数在工程和科学计算中有广泛应用。",
                "category": "数学",
                "tags": "线性代数,矩阵,必修"
            },
            {
                "title": "大学物理实验",
                "content": "大学物理实验是理工科学生的重要实践课程。通过实验可以验证物理定律，培养科学实验能力和分析能力。实验内容包括力学、热学、电磁学、光学等方面。",
                "category": "物理",
                "tags": "实验,物理,必修"
            },
            {
                "title": "计算机网络概论",
                "content": "计算机网络课程介绍互联网的基本原理和架构。包括TCP/IP协议、网络拓扑结构、网络安全等内容。理解网络原理对现代软件开发非常重要。",
                "category": "计算机",
                "tags": "网络,协议,选修"
            },
            {
                "title": "大学英语六级备考",
                "content": "大学英语六级考试难度比四级更高，要求学生具备更强的英语能力。建议多做真题，提高阅读速度和听力理解能力。重点积累高级词汇和复杂句型。",
                "category": "英语",
                "tags": "六级,英语,考试"
            },
        ]
        
        for data in knowledge_data:
            existing = db.query(Knowledge).filter(Knowledge.title == data["title"]).first()
            if not existing:
                knowledge = Knowledge(**data)
                db.add(knowledge)
                db.commit()
                print(f"✓ 创建知识: {data['title']}")
        
        # 获取所有用户
        users = db.query(User).all()
        if len(users) >= 2:
            # 创建测试问答
            questions_data = [
                {
                    "user": users[2],  # student1
                    "question": "如何学习数据结构？",
                    "answer": "学习数据结构建议：1. 理解基本概念；2. 手动画图辅助理解；3. 多编写代码实践；4. 刷算法题巩固。推荐先从线性表、栈、队列开始学习。",
                    "category": "计算机"
                },
                {
                    "user": users[2],
                    "question": "微积分和高等数学有什么区别？",
                    "answer": "微积分是高等数学的一个分支。高等数学包括微积分、线性代数、概率论等多个部分。微积分主要研究变化率和累积问题，是高等数学的核心内容之一。",
                    "category": "数学"
                },
                {
                    "user": users[3],  # student2
                    "question": "四级听力怎么提高？",
                    "answer": "提高四级听力的方法：1. 每天坚持听英语材料；2. 跟读模仿发音；3. 多做真题熟悉题型；4. 注意记笔记捕捉关键信息；5. 掌握常见词汇和表达。",
                    "category": "英语"
                },
                {
                    "user": users[3],
                    "question": "计算机网络中TCP和UDP的区别是什么？",
                    "answer": "TCP和UDP的主要区别：1. TCP是面向连接的，UDP是无连接的；2. TCP提供可靠传输，UDP不保证可靠；3. TCP有拥塞控制，UDP没有；4. TCP传输效率较低，UDP传输效率高。选择哪种协议取决于应用需求。",
                    "category": "计算机"
                },
                {
                    "user": users[4],  # student3
                    "question": "大学物理实验报告怎么写？",
                    "answer": "物理实验报告应包括：1. 实验目的和原理；2. 实验设备和步骤；3. 实验数据和记录；4. 数据处理和分析；5. 实验结论和讨论。报告要求数据准确、分析合理、结论明确。",
                    "category": "物理"
                },
            ]
            
            for data in questions_data:
                q = Question(
                    user_id=data["user"].id,
                    question=data["question"],
                    answer=data["answer"],
                    category=data["category"],
                    created_at=datetime.now()
                )
                db.add(q)
                db.commit()
                db.refresh(q)
                print(f"✓ 创建问答: {data['question']}")
            
            # 创建反馈
            questions = db.query(Question).all()
            if len(questions) >= 3:
                feedback_data = [
                    {
                        "user": users[2],
                        "question": questions[0],
                        "rating": 5,
                        "comment": "回答很详细，帮助很大！"
                    },
                    {
                        "user": users[3],
                        "question": questions[2],
                        "rating": 4,
                        "comment": "建议多给一些听力材料推荐。"
                    },
                    {
                        "user": users[4],
                        "question": questions[4],
                        "rating": 5,
                        "comment": "非常实用的建议！"
                    },
                ]
                
                for data in feedback_data:
                    feedback = Feedback(
                        user_id=data["user"].id,
                        question_id=data["question"].id,
                        rating=data["rating"],
                        comment=data["comment"]
                    )
                    db.add(feedback)
                    db.commit()
                    print(f"✓ 创建反馈: {data['user'].username} -> {data['question'].question[:20]}...")
        
        print("\n✅ 数据初始化完成！")
        print("\n默认账号：")
        print("  管理员: admin / admin123")
        print("  教师:   teacher / teacher123")
        print("  学生:   student1 / student123")
        print("          student2 / student123")
        print("          student3 / student123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化失败: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    print("开始初始化测试数据...\n")
    init_data()
