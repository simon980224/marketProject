import pandas as pd
import pygsheets
import glob
import os

def excel_col(col):
    """將列數字轉換為Excel列標籤"""
    col_str = ""
    while col:
        (col, mod) = divmod(col - 1, 26)  # 減1是因為Excel列是從1開始計算，而不是從0
        col_str = chr(mod + 65) + col_str
    return col_str

# Google Sheets 授權
key = "/Users/chenyaoxuan/Desktop/myproject/MarketProject/astute-harmony-425407-p9-826d675d86f9.json"
gc = pygsheets.authorize(service_file=key)
url = "https://docs.google.com/spreadsheets/d/1SGNEuh-FjiBxoxH73NcDELDGbSO71vhc7DbkGuKk4wo/edit#gid=1894821213"
sheet = gc.open_by_url(url)

# 讀取數據的文件夾路徑
folder_path = '/Users/chenyaoxuan/Desktop/myproject/MarketProject/marketExcel/'
marketExcel = glob.glob(os.path.join(folder_path, '**', '*.xlsx'), recursive=True)

# 初始化數據字典
market_data = {}

# 讀取每個 Excel 文件並處理數據
for excel in marketExcel:
    df = pd.read_excel(excel)
    data_list = df.values.tolist()
    transaction_details = data_list[1:-1]  # 排除標題行和總金額行
    
    # 提取文件名的前七個字作為標題
    filename = os.path.basename(excel)
    title = filename[:7]
    
    market_data[title] = transaction_details

# 將資料寫入 Google Sheets
for title, details in market_data.items():
    try:
        wks = sheet.worksheet('title', title)
    except pygsheets.WorksheetNotFound:
        # 如果工作表不存在，創建一個新的工作表
        wks = sheet.add_worksheet(title)
    
    # 清空工作表
    wks.clear()

    # 將資料寫入工作表
    df = pd.DataFrame(details, columns=["編號姓名", "時間", "銀行卡", "提款方式", "金額", "狀態"])
    wks.set_dataframe(df, (1, 1))
    print(f"資料已成功更新 Google Sheets 的 {title} 子標籤")

print("所有資料已成功備份到 Google Sheets！")