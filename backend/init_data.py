#!/usr/bin/env python
"""
初始化测试数据
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Question, Knowledge, Feedback
from app.utils import get_password_hash


def init_users(db: Session):
    """初始化用户数据"""
    users = [
        User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            real_name="系统管理员",
            role="admin",
            email="admin@example.com"
        ),
        User(
            username="teacher",
            password_hash=get_password_hash("123456"),
            real_name="张老师",
            role="teacher",
            email="teacher@example.com"
        ),
        User(
            username="student1",
            password_hash=get_password_hash("123456"),
            real_name="学生一",
            role="student",
            student_id="2021001",
            email="student1@example.com"
        ),
        User(
            username="student2",
            password_hash=get_password_hash("123456"),
            real_name="学生二",
            role="student",
            student_id="2021002",
            email="student2@example.com"
        )
    ]
    
    db.add_all(users)
    db.commit()
    print("✓ 用户数据初始化完成")
    return users


def init_knowledge(db: Session):
    """初始化知识库数据"""
    knowledges = [
        Knowledge(
            title="什么是人工智能？",
            content="人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。它包括机器学习、深度学习、自然语言处理、计算机视觉等多个子领域。",
            category="计算机科学",
            tags="人工智能,AI,机器学习"
        ),
        Knowledge(
            title="深度学习的原理是什么？",
            content="深度学习是机器学习的一个分支，它使用多层神经网络来学习数据的表示。深层神经网络能够自动学习从原始数据中提取特征，无需人工设计特征提取器。其核心原理包括：前向传播计算输出、反向传播更新参数、优化算法如梯度下降等。",
            category="计算机科学",
            tags="深度学习,神经网络"
        ),
        Knowledge(
            title="如何选择编程语言？",
            content="选择编程语言需要考虑以下因素：1）应用场景（Web开发选Python/JavaScript，系统编程选C++/Rust）；2）学习曲线（Python适合初学者）；3）生态系统和社区支持；4）性能要求；5）开发效率。初学者建议从Python开始。",
            category="计算机科学",
            tags="编程语言,学习"
        ),
        Knowledge(
            title="什么是数据库？",
            content="数据库是按照数据结构来组织、存储和管理数据的仓库。常见的数据库类型包括：关系型数据库（如MySQL、PostgreSQL）使用表格存储数据，支持SQL查询；非关系型数据库（如MongoDB、Redis）使用文档、键值等方式存储数据。选择数据库需考虑数据结构、查询需求、并发量等因素。",
            category="计算机科学",
            tags="数据库"
        ),
        Knowledge(
            title="计算机网络的基本概念",
            content="计算机网络是指将地理位置不同的具有独立功能的多台计算机及其外部设备，通过通信线路连接起来，在网络操作系统、网络管理软件及网络通信协议的管理和协调下，实现资源共享和信息传递的计算机系统。网络协议如TCP/IP是网络通信的基础。",
            category="计算机科学",
            tags="网络,TCP/IP"
        ),
        Knowledge(
            title="什么是面向对象编程？",
            content="面向对象编程（OOP）是一种编程范式，它使用对象来设计软件。核心概念包括：1）类：对象的模板；2）对象：类的实例；3）封装：隐藏内部实现细节；4）继承：子类继承父类的属性和方法；5）多态：同一方法在不同对象上有不同行为。常见的OOP语言有Java、Python、C++等。",
            category="计算机科学",
            tags="面向对象,OOP"
        ),
        Knowledge(
            title="Git版本控制基础",
            content="Git是一个分布式版本控制系统，用于跟踪代码变化。常用命令包括：git init（初始化仓库）、git add（添加文件到暂存区）、git commit（提交更改）、git push（推送到远程）、git pull（拉取更新）、git branch（分支管理）、git merge（合并分支）。GitHub和GitLab是常用的代码托管平台。",
            category="计算机科学",
            tags="Git,版本控制"
        ),
        Knowledge(
            title="Linux操作系统基础",
            content="Linux是一种开源的Unix-like操作系统。常用命令包括：ls（列出文件）、cd（切换目录）、mkdir（创建目录）、rm（删除文件）、cp（复制）、mv（移动）、grep（搜索）、chmod（修改权限）、ps（查看进程）、top（系统监控）。Linux广泛应用于服务器、嵌入式设备和开发环境。",
            category="计算机科学",
            tags="Linux,操作系统"
        ),
        Knowledge(
            title="什么是云计算？",
            content="云计算是通过互联网提供计算资源（服务器、存储、数据库等）的服务模式。主要服务类型包括：IaaS（基础设施即服务，如AWS EC2）、PaaS（平台即服务，如Google App Engine）、SaaS（软件即服务，如Google Docs）。部署模式有公有云、私有云和混合云。云计算具有弹性扩展、按需付费、降低成本等优势。",
            category="计算机科学",
            tags="云计算"
        ),
        Knowledge(
            title="如何提高编程能力？",
            content="提高编程能力的方法：1）多做项目，实践是最好的老师；2）阅读优秀代码，学习设计模式和最佳实践；3）掌握数据结构和算法基础；4）熟悉开发工具和版本控制；5）参与开源项目；6）持续学习新技术；7）学会调试和排错；8）培养代码规范意识。记住：编程是一项需要长期积累的技能。",
            category="学习指导",
            tags="编程,学习"
        )
    ]
    
    db.add_all(knowledges)
    db.commit()
    print("✓ 知识库数据初始化完成")
    return knowledges


def init_questions(db: Session, users: list):
    """初始化问答数据"""
    questions = [
        Question(
            user_id=users[2].id,  # student1
            question="Python中的列表和元组有什么区别？",
            answer="列表和元组的主要区别：1）可变性：列表可修改，元组不可修改；2）语法：列表用[]，元组用()；3）性能：元组比列表更高效；4）使用场景：列表用于可变序列，元组用于固定数据。元组可以作为字典的键，列表则不行。",
            category="Python"
        ),
        Question(
            user_id=users[2].id,
            question="什么是递归？什么时候使用递归？",
            answer="递归是函数调用自身来解决问题的方法。递归需要两个要素：1）基准情况：递归的终止条件；2）递归步骤：将问题分解为更小的子问题。适合递归的场景：树结构遍历、分治算法（如快速排序）、深度优先搜索等。注意：递归可能导致栈溢出，要控制递归深度。",
            category="算法"
        ),
        Question(
            user_id=users[3].id,  # student2
            question="数据库索引的作用是什么？",
            answer="数据库索引类似于书的目录，用于快速定位数据。索引可以大幅提高查询速度，特别是对于大表。但索引也有代价：1）占用存储空间；2）降低插入、更新、删除速度（需要维护索引）。应该为经常查询的列建立索引，但不要过度索引。MySQL使用B树索引结构。",
            category="数据库"
        ),
        Question(
            user_id=users[3].id,
            question="前端开发和后端开发有什么区别？",
            answer="前端开发：负责用户界面和交互，技术栈包括HTML、CSS、JavaScript、Vue/React等框架，关注用户体验和视觉效果。后端开发：负责服务器端逻辑、数据处理和API接口，技术栈包括Python/Java/Node.js、数据库、服务器架构等，关注性能、安全和数据处理。两者需要配合，通过API接口通信。",
            category="开发"
        ),
        Question(
            user_id=users[2].id,
            question="什么是RESTful API？",
            answer="RESTful API是一种遵循REST（表现层状态转移）架构风格的API设计原则。核心概念：1）使用HTTP方法：GET（获取）、POST（创建）、PUT（更新）、DELETE（删除）；2）资源用URI表示；3）使用JSON/XML交换数据；4）无状态：每个请求包含所有必要信息；5）统一接口。RESTful API简单易用，广泛应用于Web服务。",
            category="Web开发"
        )
    ]
    
    db.add_all(questions)
    db.commit()
    print("✓ 问答数据初始化完成")
    return questions


def init_feedbacks(db: Session, questions: list, users: list):
    """初始化反馈数据"""
    feedbacks = [
        Feedback(
            user_id=users[2].id,
            question_id=questions[0].id,
            rating=5,
            comment="回答很详细，容易理解！"
        ),
        Feedback(
            user_id=users[3].id,
            question_id=questions[2].id,
            rating=4,
            comment="帮助很大，希望能多一些例子"
        ),
        Feedback(
            user_id=users[2].id,
            question_id=questions[1].id,
            rating=5,
            comment="清晰明了，解决了我的困惑"
        )
    ]
    
    db.add_all(feedbacks)
    db.commit()
    print("✓ 反馈数据初始化完成")


if __name__ == "__main__":
    print("=" * 50)
    print("开始初始化测试数据...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(User).count() > 0:
            print("⚠ 数据库中已存在数据，请先运行 reset_data.py 清空数据")
            db.close()
            exit(1)
        
        users = init_users(db)
        knowledges = init_knowledge(db)
        questions = init_questions(db, users)
        init_feedbacks(db, questions, users)
        
        print("\n" + "=" * 50)
        print("测试数据初始化完成！")
        print("=" * 50)
        print("\n测试账号：")
        print("  管理员: admin / admin123")
        print("  教师:   teacher / 123456")
        print("  学生1:  student1 / 123456")
        print("  学生2:  student2 / 123456")
    except Exception as e:
        print(f"\n初始化失败: {e}")
        db.rollback()
    finally:
        db.close()
