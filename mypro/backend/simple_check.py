import requests
import json

r = requests.get('http://localhost:8000/openapi.json')
data = r.json()

print("Profile-changes routes:")
for path in data['paths']:
    if 'profile' in path.lower():
        print(f"  {path}")
        for method in data['paths'][path]:
            print(f"    {method.upper()}")
