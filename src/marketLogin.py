from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import time

# 設置 Chrome WebDriver 的路徑
service = Service('/Users/chenyaoxuan/Desktop/chromedriver')
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)

# 讀取和處理 cookies
with open('/Users/chenyaoxuan/Desktop/myproject/cookies.json', 'r', encoding='utf-8') as file:
    cookies_list = json.load(file)

# 複製一份 cookies_list 用於追蹤未添加的 cookies
remaining_cookies = cookies_list.copy()

# 設置 https://shopee.tw/ 的 Cookie
driver.get('https://shopee.tw/')
for cookie in cookies_list:
    if cookie['domain'] == '.shopee.tw':
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'strict':
                cookie['sameSite'] = 'Strict'
            elif cookie['sameSite'] == 'lax':
                cookie['sameSite'] = 'Lax'
            elif cookie['sameSite'] is None:
                cookie['sameSite'] = 'None'
        driver.add_cookie(cookie)
        remaining_cookies.remove(cookie)

# 刷新頁面以應用 cookies
driver.refresh()
time.sleep(7)  # 等待幾秒以確保 cookies 被應用

# 設置 https://seller.shopee.tw/ 的 Cookie
driver.get('https://seller.shopee.tw/')
for cookie in cookies_list:
    if cookie['domain'] == 'seller.shopee.tw':
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'strict':
                cookie['sameSite'] = 'Strict'
            elif cookie['sameSite'] == 'lax':
                cookie['sameSite'] = 'Lax'
            elif cookie['sameSite'] is None:
                cookie['sameSite'] = 'None'
        driver.add_cookie(cookie)
        remaining_cookies.remove(cookie)

# 刷新頁面以應用 cookies
driver.refresh()
time.sleep(7)  # 等待幾秒以確保 cookies 被應用

# 打印未加入的 cookies
print("Remaining cookies that were not added:")
for cookie in remaining_cookies:
    print(cookie)
    
driver.get('https://shopee.tw/')

# 等待一段时间以确保 cookies 被应用
time.sleep(999999)

# 你可以在此添加其他操作，例如導航到其他頁面等

# 關閉瀏覽器
driver.quit()