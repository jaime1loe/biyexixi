import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("Adding missing columns to questions table...")

try:
    cursor.execute("ALTER TABLE questions ADD COLUMN views INT DEFAULT 0 AFTER category")
    print("[OK] Added 'views' column")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("ALTER TABLE questions ADD COLUMN is_public INT DEFAULT 1 AFTER views")
    print("[OK] Added 'is_public' column")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("ALTER TABLE questions ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at")
    print("[OK] Added 'updated_at' column")
except Exception as e:
    print(f"Note: {e}")

conn.commit()

# Verify
cursor.execute("DESCRIBE questions")
columns = cursor.fetchall()

print("\nUpdated questions table structure:")
for col in columns:
    print(f"  {col[0]}: {col[1]}")

cursor.close()
conn.close()

print("\n[OK] Database tables fixed!")
