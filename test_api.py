import requests

# 测试考试API
try:
    response = requests.get('http://localhost:5000/api/exams/')
    print('Status Code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))