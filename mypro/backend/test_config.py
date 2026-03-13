import sys
sys.path.insert(0, '.')
from app.config import settings

print("Configuration loaded:")
print("Database URL:", settings.DATABASE_URL)

try:
    from app.database import engine
    print("Engine created successfully")

    with engine.connect() as conn:
        print("Database connection successful!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
