from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# 設置 Chrome WebDriver 的路徑
service = Service('/Users/chenyaoxuan/Desktop/chromedriver')
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)

userName = 'willy200899'
passWord = 'Chen54321.'

# 讀取和處理 cookies
with open('/Users/chenyaoxuan/Desktop/myproject/marketProject/cookies/A27.json', 'r', encoding='utf-8') as file:
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
        try:
            driver.add_cookie(cookie)
            remaining_cookies.remove(cookie)
        except Exception as e:
            print(f"Error adding cookie: {cookie}")
            print(e)
time.sleep(5)

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
        try:
            driver.add_cookie(cookie)
            remaining_cookies.remove(cookie)
        except Exception as e:
            print(f"Error adding cookie: {cookie}")
            print(e)
time.sleep(5)

# 打印未加入的 cookies
print("Remaining cookies that were not added:")
for cookie in remaining_cookies:
    print(cookie)

driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/form/div[2]/div[1]/input').send_keys(passWord)
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/form/div[1]/div[1]/input').send_keys(userName)
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/form/button').click()

time.sleep(5)

# 轉跳到 wallet 頁面
driver.get('https://seller.shopee.tw/portal/finance/wallet/shopeepay')

# 使用顯式等待來確保元素存在
wait = WebDriverWait(driver, 10)

# 嘗試找到並輸入密碼
try:
    wallet_password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/form/div[2]/div/div/div/div/input'))
    )
    wallet_password_input.send_keys(passWord)

    # 點擊確認按鈕
    confirm_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/form/div[3]/button[2]'))
    )
    confirm_button.click()
except Exception as e:
    print("未找到密碼輸入框或確認按鈕，跳過該步驟")
    pass

# 關閉瀏覽器
time.sleep(999999)
driver.quit()