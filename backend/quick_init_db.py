#!/usr/bin/env python
"""
快速数据库初始化脚本 - 直接执行SQL
"""
import subprocess
import os


def create_database_sql():
    """创建SQL文件"""
    sql_content = """-- 创建数据库
CREATE DATABASE IF NOT EXISTS qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE qa_system;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    real_name VARCHAR(50) COMMENT '真实姓名',
    student_id VARCHAR(20) UNIQUE COMMENT '学号',
    email VARCHAR(100) COMMENT '邮箱',
    role VARCHAR(20) DEFAULT 'student' COMMENT '角色: student/teacher/admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 问题表
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '问题ID',
    user_id INT NOT NULL COMMENT '用户ID',
    question TEXT NOT NULL COMMENT '问题内容',
    answer TEXT COMMENT '答案内容',
    category VARCHAR(50) COMMENT '问题分类',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问题表';

-- 反馈评价表
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '反馈ID',
    user_id INT NOT NULL COMMENT '用户ID',
    question_id INT NOT NULL COMMENT '问题ID',
    rating INT NOT NULL COMMENT '评分: 1-5星',
    comment TEXT COMMENT '评价内容',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_question_id (question_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='反馈评价表';

-- 知识库表
CREATE TABLE IF NOT EXISTS knowledge (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '知识ID',
    title VARCHAR(200) NOT NULL COMMENT '知识标题',
    content TEXT NOT NULL COMMENT '知识内容',
    category VARCHAR(50) COMMENT '分类',
    tags VARCHAR(200) COMMENT '标签，逗号分隔',
    file_path VARCHAR(255) COMMENT '关联文件路径',
    embedding TEXT COMMENT '向量数据(JSON)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库表';

-- 统计表
CREATE TABLE IF NOT EXISTS statistics (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '统计ID',
    date VARCHAR(10) UNIQUE NOT NULL COMMENT '日期',
    question_count INT DEFAULT 0 COMMENT '问题数',
    user_count INT DEFAULT 0 COMMENT '活跃用户数',
    avg_rating FLOAT DEFAULT 0.0 COMMENT '平均评分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='统计表';

-- 显示所有表
SHOW TABLES;
"""
    
    with open('init_database.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    print("✓ SQL文件已创建: init_database.sql")
    return 'init_database.sql'


def execute_mysql_command(sql_file):
    """使用MySQL命令行执行SQL"""
    try:
        # 尝试使用mysql命令
        result = subprocess.run(
            ['mysql', '-u', 'root', '-e', f'source {os.path.abspath(sql_file)}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ 数据库创建成功！")
            print(result.stdout)
            return True
        else:
            print(f"✗ MySQL命令执行失败: {result.stderr}")
            return False
    except FileNotFoundError:
        print("⚠ 未找到mysql命令，请手动执行SQL文件")
        return False
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("快速初始化数据库")
    print("=" * 50)
    
    sql_file = create_database_sql()
    
    print("\n" + "=" * 50)
    print("SQL文件已生成")
    print("=" * 50)
    print("\n请按以下方式之一执行SQL：")
    print("\n方法1 - 使用MySQL命令行:")
    print(f"  mysql -u root < {sql_file}")
    print("\n方法2 - 使用MySQL Workbench:")
    print(f"  打开文件并执行: {os.path.abspath(sql_file)}")
    print("\n方法3 - 在MySQL客户端中:")
    print(f"  source {os.path.abspath(sql_file)}")
    print("\n方法4 - 本程序自动执行:")
    print("  python quick_init_db.py --exec")
    
    import sys
    if '--exec' in sys.argv:
        execute_mysql_command(sql_file)
