from app.database import engine
from sqlalchemy import text

conn = engine.connect()
result = conn.execute(text('SELECT id, username, role FROM users WHERE role="admin"'))
for row in result:
    print(row)
conn.close()
