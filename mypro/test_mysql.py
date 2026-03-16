import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.config import settings
    print("数据库配置:")
    print(f"主机: {settings.DB_HOST}")
    print(f"端口: {settings.DB_PORT}")
    print(f"数据库名: {settings.DB_NAME}")
    print(f"用户名: {settings.DB_USER}")
    print(f"密码长度: {len(settings.DB_PASSWORD)}")
    
    # 测试MySQL连接
    import pymysql
    
    print("\n尝试连接MySQL...")
    try:
        conn = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            connect_timeout=10
        )
        print("[OK] MySQL连接成功!")
        
        # 检查表
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"数据库中有 {len(tables)} 个表:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # 检查users表
            cursor.execute("SELECT * FROM users LIMIT 3")
            users = cursor.fetchall()
            if users:
                print("\nusers表前3条记录:")
                for user in users:
                    print(f"  ID: {user[0]}, 用户名: {user[1]}, 角色: {user[3] if len(user) > 3 else 'N/A'}")
            else:
                print("\n[WARNING] users表为空或无记录")
                
        conn.close()
        
    except pymysql.Error as e:
        print(f"[ERROR] MySQL连接失败: {e}")
        
        # 尝试不指定数据库的连接
        print("\n尝试不指定数据库的连接...")
        try:
            conn = pymysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                connect_timeout=5
            )
            print("[OK] MySQL服务器连接成功，但数据库可能不存在")
            
            # 检查数据库是否存在
            with conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                print(f"可用的数据库: {databases}")
                
                if settings.DB_NAME in databases:
                    print(f"[OK] 数据库 '{settings.DB_NAME}' 存在")
                else:
                    print(f"[ERROR] 数据库 '{settings.DB_NAME}' 不存在")
                    print("请运行 create_tables.py 创建数据库")
                    
            conn.close()
        except pymysql.Error as e2:
            print(f"[ERROR] 无法连接到MySQL服务器: {e2}")
            print("请确保MySQL服务已启动")
            
except Exception as e:
    print(f"[ERROR] 检查失败: {e}")
    import traceback
    traceback.print_exc()