from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Test hash from database
hash_from_db = '$5$rounds=535000$Xkg4VvIF5yTX9WFx$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8'

# Verify password
result = pwd_context.verify('123456', hash_from_db)
print(f"Password verification result: {result}")

# Generate new hash for '123456'
new_hash = pwd_context.hash('123456')
print(f"New hash: {new_hash}")
