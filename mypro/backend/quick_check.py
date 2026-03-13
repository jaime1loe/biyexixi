import sys
sys.path.insert(0, '.')
import pymysql

print("Testing MySQL connection...")
print("=" * 50)

# Test 1: Check if pymysql is installed
try:
    print("1. pymysql version:", pymysql.__version__)
except:
    print("1. pymysql not installed")
    sys.exit(1)

# Test 2: Try to connect to MySQL
print("\n2. Testing MySQL connection to localhost:3306")
try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='20040618',
        connect_timeout=5
    )
    print("   Connected to MySQL server successfully!")
    conn.close()
except Exception as e:
    print(f"   ERROR: {e}")
    print("\nPlease check:")
    print("   - Is MySQL service running?")
    print("   - Is the password correct? (20040618)")
    sys.exit(1)

# Test 3: Check if database exists
print("\n3. Checking database 'qa_system'")
try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='20040618',
        database='qa_system',
        connect_timeout=5
    )
    print("   Database 'qa_system' exists!")
    conn.close()
except Exception as e:
    if "Unknown database" in str(e):
        print("   ERROR: Database 'qa_system' does not exist!")
        print("\nPlease create it:")
        print("   CREATE DATABASE qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    else:
        print(f"   ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("All tests passed! Database connection is OK.")
