import requests
from bs4 import BeautifulSoup
import json

# 忽略SSL警告
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 創建會話
session = requests.Session()

# 訪問登錄頁面以獲取CSRF令牌
login_page_url = "https://localhost:7229/account/login"
login_page_response = session.get(login_page_url, verify=False)

# 解析HTML以獲取__RequestVerificationToken
soup = BeautifulSoup(login_page_response.text, 'html.parser')
csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

# 登錄URL
login_url = "https://localhost:7229/account/login"

# 請求頭
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://localhost:7229",
    "Pragma": "no-cache",
    "Referer": "https://localhost:7229/account/login",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
}

# 登錄數據
data = {
    "UserName": "edenred",
    "Password": "edenred",
    "__RequestVerificationToken": csrf_token
}

# 發送POST請求進行登錄
login_response = session.post(login_url, headers=headers, data=data, verify=False)

# 打印登錄響應狀態碼和內容
print("Login Status Code:", login_response.status_code)
print("Login Response Text:", login_response.text)

# 假設令牌在響應體中以JSON格式返回
jwt_token = None
try:
    response_json = login_response.json()
    jwt_token = response_json.get('token')
    print("JWT Token:", jwt_token)
except json.JSONDecodeError:
    print("No JSON response")

if jwt_token:
    # 使用獲取的JWT令牌訪問受保護的API端點
    protected_url = "https://localhost:7229/api/protected"  # 替換為你的受保護API端點

    # 設置Authorization標頭
    protected_headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # 發送GET請求到受保護的API端點
    protected_response = session.get(protected_url, headers=protected_headers, verify=False)

    # 打印受保護API響應狀態碼和內容
    print("Protected API Status Code:", protected_response.status_code)
    print("Protected API Response Text:", protected_response.text)
else:
    print("JWT Token not found in the response")