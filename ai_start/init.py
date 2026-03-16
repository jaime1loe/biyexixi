import pymysql
import os

# Change to project directory
os.chdir(r'C:\Users\1\Desktop\毕业实习\jaime1loe-biyexixi-03d1de7\jaime1loe-biyexixi-03d1de7')

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("Creating database qa_system...")
cursor.execute("CREATE DATABASE IF NOT EXISTS qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
conn.commit()
print("[OK] Database created")

cursor.execute("USE qa_system")

# Create tables
print("\nCreating tables...")

# Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    real_name VARCHAR(50),
    student_id VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    phone VARCHAR(20),
    avatar VARCHAR(255),
    role VARCHAR(20) DEFAULT 'student',
    department VARCHAR(50),
    major VARCHAR(50),
    class_name VARCHAR(50),
    is_active INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)''')

# Questions table
cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    category VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)''')

# Feedbacks table
cursor.execute('''CREATE TABLE IF NOT EXISTS feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
)''')

# Knowledge table
cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    tags VARCHAR(200),
    file_path VARCHAR(255),
    embedding TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)''')

# Statistics table
cursor.execute('''CREATE TABLE IF NOT EXISTS statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(10) UNIQUE NOT NULL,
    question_count INT DEFAULT 0,
    user_count INT DEFAULT 0,
    avg_rating FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()
print("[OK] Tables created")

# Insert test data
print("\nInserting test data...")

# Password hash for '123456'
# Using SHA-256 with salt 'qa_system'
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insert admin
cursor.execute("INSERT IGNORE INTO users (username, password_hash, real_name, role) VALUES (%s, %s, %s, %s)",
    ('admin', hash_password('123456'), 'Administrator', 'admin'))

# Insert student
cursor.execute("INSERT IGNORE INTO users (username, password_hash, real_name, student_id, role) VALUES (%s, %s, %s, %s, %s)",
    ('student', hash_password('123456'), 'Test Student', '2024001', 'student'))

conn.commit()
print("[OK] Test data inserted")

cursor.close()
conn.close()

print("\n" + "="*50)
print("Database initialization complete!")
print("="*50)
print("Test accounts:")
print("  Student: student / 123456")
print("  Admin: admin / 123456")
print("="*50)
