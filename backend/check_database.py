"""
数据库连接诊断脚本
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

def step1_check_mysql_module():
    """步骤1：检查pymysql模块"""
    print("=" * 60)
    print("步骤1：检查MySQL驱动")
    print("=" * 60)
    try:
        import pymysql
        print("✓ pymysql模块已安装")
        print(f"  版本: {pymysql.__version__}")
        return True
    except ImportError as e:
        print(f"✗ pymysql模块未安装")
        print(f"  错误信息: {e}")
        print(f"  解决方案: pip install pymysql")
        return False

def step2_check_config():
    """步骤2：检查配置"""
    print("\n" + "=" * 60)
    print("步骤2：检查数据库配置")
    print("=" * 60)
    try:
        from app.config import settings
        print(f"✓ 配置文件加载成功")
        print(f"  数据库主机: {settings.DB_HOST}")
        print(f"  数据库端口: {settings.DB_PORT}")
        print(f"  数据库名称: {settings.DB_NAME}")
        print(f"  用户名: {settings.DB_USER}")
        print(f"  密码: {'*' * len(settings.DB_PASSWORD)}")
        print(f"  完整连接字符串: {settings.DATABASE_URL}")
        return True, settings
    except Exception as e:
        print(f"✗ 配置文件加载失败")
        print(f"  错误信息: {e}")
        return False, None

def step3_test_connection(settings):
    """步骤3：测试数据库连接"""
    print("\n" + "=" * 60)
    print("步骤3：测试数据库连接")
    print("=" * 60)
    try:
        import pymysql

        # 尝试直接连接
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            connect_timeout=5
        )
        print(f"✓ 成功连接到MySQL服务器")
        connection.close()

        # 尝试连接到指定数据库
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            connect_timeout=5
        )
        print(f"✓ 成功连接到数据库 '{settings.DB_NAME}'")
        connection.close()
        return True

    except pymysql.err.OperationalError as e:
        error_code = e.args[0]
        error_msg = e.args[1]

        if error_code == 2003:
            print(f"✗ 无法连接到MySQL服务器")
            print(f"  错误信息: {error_msg}")
            print(f"\n  可能原因:")
            print(f"  1. MySQL服务未启动")
            print(f"  2. 主机地址 {settings.DB_HOST} 不正确")
            print(f"  3. 端口 {settings.DB_PORT} 不正确")
            print(f"\n  解决方案:")
            print(f"  - Windows: 在服务管理器中启动MySQL服务")
            print(f"  - 或者运行: net start mysql")

        elif error_code == 1045:
            print(f"✗ 数据库认证失败")
            print(f"  错误信息: {error_msg}")
            print(f"\n  可能原因:")
            print(f"  1. 用户名或密码不正确")
            print(f"  2. 当前配置密码: {'*' * len(settings.DB_PASSWORD)}")
            print(f"\n  解决方案:")
            print(f"  - 检查MySQL密码是否为: 12345678")
            print(f"  - 如需修改密码,请编辑 backend/app/config.py")

        elif error_code == 1049:
            print(f"✗ 数据库不存在")
            print(f"  错误信息: {error_msg}")
            print(f"\n  解决方案:")
            print(f"  1. 打开MySQL命令行或客户端")
            print(f"  2. 执行: CREATE DATABASE {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

        else:
            print(f"✗ 数据库连接错误")
            print(f"  错误代码: {error_code}")
            print(f"  错误信息: {error_msg}")

        return False

    except Exception as e:
        print(f"✗ 未知错误")
        print(f"  错误信息: {e}")
        return False

def step4_check_sqlalchemy():
    """步骤4：检查SQLAlchemy连接"""
    print("\n" + "=" * 60)
    print("步骤4：检查SQLAlchemy连接")
    print("=" * 60)
    try:
        from app.database import engine

        # 测试连接
        with engine.connect() as conn:
            print(f"✓ SQLAlchemy引擎连接成功")

        # 测试查询
        with engine.connect() as conn:
            result = conn.execute("SELECT VERSION()")
            version = result.fetchone()[0]
            print(f"  MySQL版本: {version}")

        return True

    except Exception as e:
        print(f"✗ SQLAlchemy连接失败")
        print(f"  错误信息: {e}")
        return False

def step5_check_tables():
    """步骤5：检查数据表"""
    print("\n" + "=" * 60)
    print("步骤5：检查数据表")
    print("=" * 60)
    try:
        from app.database import engine, Base

        # 显示所有表
        with engine.connect() as conn:
            result = conn.execute(f"SHOW TABLES FROM qa_system")
            tables = [row[0] for row in result.fetchall()]

            if tables:
                print(f"✓ 数据库中存在 {len(tables)} 张表:")
                for table in tables:
                    print(f"  - {table}")
            else:
                print(f"⚠ 数据库中没有表")
                print(f"  系统会在首次运行时自动创建表")

        return True

    except Exception as e:
        print(f"✗ 检查表失败")
        print(f"  错误信息: {e}")
        return False

def main():
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  数据库连接诊断工具".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)

    # 执行检查步骤
    results = []

    results.append(("pymysql模块", step1_check_mysql_module()))

    config_ok, settings = step2_check_config()
    results.append(("配置加载", config_ok))

    if config_ok and settings:
        results.append(("数据库连接", step3_test_connection(settings)))
        results.append(("SQLAlchemy", step4_check_sqlalchemy()))
        results.append(("数据表", step5_check_tables()))

    # 显示总结
    print("\n" + "=" * 60)
    print("诊断总结")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status:8} - {name}")
        if not result:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有检查通过!数据库连接正常")
        print("\n可以运行启动系统.bat启动服务")
    else:
        print("✗ 部分检查未通过,请根据上述提示解决问题")
        print("\n常见问题解决方案:")
        print("1. MySQL未启动: 打开服务管理器启动MySQL服务")
        print("2. 密码错误: 确认MySQL root密码为 12345678")
        print("3. 数据库不存在: 执行 CREATE DATABASE qa_system CHARACTER SET utf8mb4;")
    print("=" * 60)

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
