"""
检查profile_changes表是否存在
"""
import sys
import io
from pathlib import Path

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine
from sqlalchemy import text

def check_profile_changes_table():
    """检查profile_changes表"""
    print("=" * 60)
    print("检查 profile_changes 表")
    print("=" * 60)

    try:
        with engine.connect() as conn:
            # 检查表是否存在 (MySQL语法)
            result = conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = DATABASE() AND table_name = 'profile_change_requests'
            """))
            table_exists = result.fetchone()[0] > 0

            if table_exists:
                print("✓ profile_change_requests 表存在")

                # 查看表结构
                result = conn.execute(text("DESCRIBE profile_change_requests"))
                columns = result.fetchall()
                print("\n表结构:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")

                # 查看数据数量
                result = conn.execute(text("SELECT COUNT(*) FROM profile_change_requests"))
                count = result.fetchone()[0]
                print(f"\n表中共有 {count} 条记录")

                # 如果有数据，显示最近的几条
                if count > 0:
                    result = conn.execute(text("""
                        SELECT * FROM profile_change_requests
                        ORDER BY created_at DESC
                        LIMIT 5
                    """))
                    rows = result.fetchall()
                    print("\n最近5条记录:")
                    for row in rows:
                        print(f"  ID: {row[0]}, 用户ID: {row[1]}, 状态: {row[9]}")

            else:
                print("✗ profile_change_requests 表不存在")
                print("\n正在创建表...")

                # 创建表 (MySQL语法)
                conn.execute(text("""
                    CREATE TABLE profile_change_requests (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        real_name VARCHAR(100),
                        email VARCHAR(100),
                        phone VARCHAR(20),
                        department VARCHAR(100),
                        major VARCHAR(100),
                        bio TEXT,
                        reason TEXT NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        admin_comment TEXT,
                        reviewed_by INT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        reviewed_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (reviewed_by) REFERENCES users(id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                conn.commit()
                print("✓ profile_change_requests 表创建成功")

            # 检查users表 (MySQL语法)
            result = conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = DATABASE() AND table_name = 'users'
            """))
            users_exists = result.fetchone()[0] > 0

            if users_exists:
                print("\n✓ users 表存在")

                # 查看users表结构
                result = conn.execute(text("DESCRIBE users"))
                columns = result.fetchall()
                print("\nusers表结构:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            else:
                print("\n✗ users 表不存在")

    except Exception as e:
        print(f"✗ 检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_profile_changes_table()
