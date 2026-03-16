# -*- coding: utf-8 -*-
from app.database import engine
from sqlalchemy import text
from app.utils import get_password_hash

conn = engine.connect()
hashed = get_password_hash("12345678")
conn.execute(text('UPDATE users SET password_hash = :pwd WHERE username = "admin"'), {"pwd": hashed})
conn.commit()
print("admin password reset to 12345678")
conn.close()
