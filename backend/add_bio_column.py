"""
为 users 表添加 bio 字段
"""
import pymysql

# 数据库配置
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "qa_system"

def add_bio_column():
    """添加 bio 字段到 users 表"""
    print("=" * 60)
    print("为 users 表添加 bio 字段")
    print("=" * 60)

    try:
        # 连接数据库
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # 检查 bio 字段是否已存在
            cursor.execute("SHOW COLUMNS FROM users LIKE 'bio'")
            result = cursor.fetchone()

            if result:
                print("\n[信息] bio 字段已存在，无需添加")
            else:
                print("\n[添加] 正在添加 bio 字段...")
                cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT COMMENT '个人简介'")
                connection.commit()
                print("[成功] bio 字段添加成功！")

            # 显示 users 表结构
            print("\nusers 表结构:")
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col['Field']}: {col['Type']} {col['Null']} {col['Key']}")

    except Exception as e:
        print(f"\n[失败] 操作失败: {e}")
        raise
    finally:
        connection.close()

    print("\n" + "=" * 60)
    print("操作完成！")
    print("=" * 60)

if __name__ == '__main__':
    add_bio_column()
