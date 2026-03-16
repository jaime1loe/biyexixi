import requests

# Test login
print("Testing login...")
resp = requests.post('http://localhost:8000/api/auth/login', json={'username':'student','password':'123456'})
print(f"Login status: {resp.status_code}")
if resp.status_code == 200:
    token = resp.json()['access_token']
    print(f"Token: {token[:50]}...")
    
    # Test questions API with token
    print("\nTesting questions API...")
    headers = {'Authorization': f'Bearer {token}'}
    resp2 = requests.post('http://localhost:8000/api/questions/', headers=headers, json={'question':'hello','category':''})
    print(f"Questions API status: {resp2.status_code}")
    print(f"Response: {resp2.text[:200]}")
else:
    print(f"Error: {resp.text}")
