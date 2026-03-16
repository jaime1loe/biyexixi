from app.database import engine
from sqlalchemy import text

# 连接数据库
conn = engine.connect()

# 查看所有修改申请
result = conn.execute(text('SELECT id, user_id, status FROM profile_change_requests'))
rows = [(row[0], row[1], row[2]) for row in result]
print('数据库中的修改申请:')
for row in rows:
    print(f'  ID: {row[0]}, User ID: {row[1]}, Status: {row[2]}')

conn.close()
