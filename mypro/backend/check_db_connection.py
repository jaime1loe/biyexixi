"""
检查后端数据库连接
"""
import pymysql
from app.config import settings

def check_database_connection():
    """检查数据库连接"""
    print("=" * 60)
    print("数据库连接检查")
    print("=" * 60)

    try:
        # 连接数据库
        print(f"\n正在连接数据库...")
        print(f"主机: {settings.DB_HOST}")
        print(f"端口: {settings.DB_PORT}")
        print(f"数据库: {settings.DB_NAME}")
        print(f"用户: {settings.DB_USER}")

        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )

        print("\n[成功] 数据库连接成功!")

        # 获取数据库信息
        with connection.cursor() as cursor:
            # 检查数据库版本
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"\nMySQL 版本: {version[0]}")

            # 列出所有表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n数据库中的表 ({len(tables)} 个):")
            for table in tables:
                print(f"  - {table[0]}")

            # 检查 users 表
            print("\nusers 表统计:")
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()
            print(f"  总用户数: {user_count[0]}")

            cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
            roles = cursor.fetchall()
            print("  按角色统计:")
            for role, count in roles:
                print(f"    - {role}: {count}")

            # 检查 questions 表
            cursor.execute("SELECT COUNT(*) FROM questions")
            question_count = cursor.fetchone()
            print(f"\nquestions 表: {question_count[0]} 条记录")

            # 检查 profile_change_requests 表
            cursor.execute("SELECT COUNT(*) FROM profile_change_requests")
            profile_count = cursor.fetchone()
            print(f"profile_change_requests 表: {profile_count[0]} 条记录")

    except pymysql.Error as e:
        print(f"\n[失败] 数据库连接失败!")
        print(f"错误代码: {e.args[0]}")
        print(f"错误信息: {e.args[1]}")
    except Exception as e:
        print(f"\n[失败] 发生未知错误: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("\n数据库连接已关闭")

    print("\n" + "=" * 60)
    print("检查完成!")
    print("=" * 60)

if __name__ == '__main__':
    check_database_connection()
