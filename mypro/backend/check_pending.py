from app.database import engine
from sqlalchemy import text

# 连接数据库
conn = engine.connect()

# 查看所有修改申请的完整信息
result = conn.execute(text('SELECT id, user_id, status, real_name FROM profile_change_requests WHERE status = "pending"'))
rows = [dict(row._mapping) for row in result]
print('待审核的修改申请:')
for row in rows:
    print(f'  ID: {row["id"]}, User ID: {row["user_id"]}, Status: {row["status"]}, Real Name: {row["real_name"]}')

conn.close()
