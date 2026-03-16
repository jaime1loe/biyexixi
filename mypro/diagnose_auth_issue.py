import requests
import json

print('=== 彻底诊断认证问题 ===')

# 测试后端直接访问
backend_url = 'http://localhost:8000'

# 1. 先测试登录获取token
print('1. 测试登录获取token...')
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    # 直接调用后端API
    response = requests.post(f'{backend_url}/api/auth/login', json=login_data)
    print(f'   后端登录状态码: {response.status_code}')
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f'   获取到token: {token[:30]}...')
        
        # 2. 测试后端问答接口
        print('2. 测试后端问答接口...')
        headers = {'Authorization': f'Bearer {token}'}
        
        # 测试我的问题接口
        qa_response = requests.get(f'{backend_url}/api/questions/my?skip=0&limit=10', headers=headers)
        print(f'   我的问题接口状态码: {qa_response.status_code}')
        
        if qa_response.status_code == 200:
            questions = qa_response.json()
            print(f'   成功获取到 {len(questions)} 个问题')
            for q in questions[:3]:
                print(f'   - {q["question"][:50]}...')
        else:
            print(f'   错误详情: {qa_response.text}')
            
        # 3. 测试前端代理访问
        print('3. 测试前端代理访问...')
        frontend_url = 'http://localhost:5173'
        
        # 通过前端代理访问
        proxy_response = requests.get(f'{frontend_url}/api/questions/my?skip=0&limit=10', headers=headers)
        print(f'   前端代理状态码: {proxy_response.status_code}')
        
        if proxy_response.status_code == 200:
            print('   前端代理访问成功!')
        else:
            print(f'   前端代理错误: {proxy_response.text}')
            
        # 4. 检查token验证
        print('4. 检查token验证...')
        # 测试当前用户信息接口
        user_response = requests.get(f'{backend_url}/api/auth/me', headers=headers)
        print(f'   用户信息接口状态码: {user_response.status_code}')
        
        if user_response.status_code == 200:
            user_info = user_response.json()
            print(f'   当前用户: {user_info["username"]} (ID: {user_info["id"]})')
        else:
            print(f'   用户信息错误: {user_response.text}')
            
    else:
        print(f'   登录失败: {response.text}')
        
except Exception as e:
    print(f'   请求异常: {e}')

print('\n=== 诊断完成 ===')

# 5. 检查数据库中的用户状态
print('5. 检查数据库用户状态...')
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    from app.database import SessionLocal
    from app.models import User
    
    db = SessionLocal()
    admin_user = db.query(User).filter(User.username == 'admin').first()
    
    if admin_user:
        print(f'   admin用户存在，ID: {admin_user.id}')
        print(f'   密码哈希: {admin_user.password_hash[:30]}...')
        print(f'   角色: {admin_user.role}')
    else:
        print('   admin用户不存在!')
        
    db.close()
    
except Exception as e:
    print(f'   数据库检查失败: {e}')

print('\n=== 完整诊断结束 ===')