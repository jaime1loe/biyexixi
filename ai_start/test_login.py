import requests

# Test login
response = requests.post(
    'http://localhost:8000/api/auth/login',
    json={'username': 'student', 'password': '123456'}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
