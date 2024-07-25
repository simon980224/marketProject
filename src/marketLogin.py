from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time

# 設置 Chrome WebDriver 的路徑
service = Service('/Users/chenyaoxuan/Desktop/chromedriver')
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)

userName = '0962043673'
passWord = 'Aa532466'

# 讀取和處理 cookies
with open('/Users/chenyaoxuan/Desktop/myproject/marketProject/cookies/李伊霖.json', 'r', encoding='utf-8') as file:
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
time.sleep(7)
# driver.refresh()

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
time.sleep(7)
# driver.refresh()

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


driver.get('https://seller.shopee.tw/portal/finance/wallet/shopeepay')

driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/form/div[2]/div/div/div/div/input').send_keys(passWord)

driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/form/div[3]/button[2]').click()

# 關閉瀏覽器
time.sleep(999999)
driver.quit()