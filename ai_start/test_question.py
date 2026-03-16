import requests

# First login to get token
login_resp = requests.post(
    'http://localhost:8000/api/auth/login',
    json={'username': 'student', 'password': '123456'}
)
token = login_resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Send a question
resp = requests.post(
    'http://localhost:8000/api/questions/',
    headers=headers,
    json={
        'question': '什么是毕业实习？',
        'category': '就业指导'
    }
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
