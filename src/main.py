import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

import pandas as pd
import pygsheets
from openpyxl import load_workbook
from openpyxl.styles import Font

def execute_script(script_path):
    """運行指定的Python腳本並返回其輸出"""
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"運行腳本 {script_path} 時出現錯誤: {e}")
        return None

def load_user_info(json_path):
    """從指定的JSON文件加載用戶信息"""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"加載用戶信息文件 {json_path} 時出現錯誤: {e}")
        return None

def adjust_excel_format(file_path, font_size=20):
    """設置Excel文件中的字體大小，將「銀行卡」欄位寬度設置為50，其他欄位設置為25，行高設置為50"""
    workbook = load_workbook(file_path)
    sheet = workbook.active
    
    for row in sheet.iter_rows():
        for cell in row:
            cell.font = Font(size=font_size)
    
    # 設置列寬
    for col in sheet.columns:
        if col[0].value == "銀行卡":
            sheet.column_dimensions[col[0].column_letter].width = 50
        else:
            sheet.column_dimensions[col[0].column_letter].width = 25
    
    # 設置行高
    for row in sheet.iter_rows():
        sheet.row_dimensions[row[0].row].height = 50
    
    workbook.save(file_path)

def update_google_sheets(data, sheet):
    """將數據寫入Google Sheets"""
    for title, details in data.items():
        try:
            wks = sheet.worksheet('title', title)
        except pygsheets.WorksheetNotFound:
            wks = sheet.add_worksheet(title)
        
        wks.clear()
        df = pd.DataFrame(details, columns=["編號姓名", "時間", "銀行卡", "提款方式", "金額", "狀態"])
        wks.set_dataframe(df, (1, 1))
        print(f"{title}資料已成功更新")

def main():
    script_directory = '/Users/chenyaoxuan/Desktop/myproject/MarketProject/src/scripts'
    user_info_path = '/Users/chenyaoxuan/Desktop/myproject/MarketProject/userInfo.json'
    output_base_directory = '/Users/chenyaoxuan/Desktop/myproject/MarketProject/marketExcel'
    
    scripts = [f for f in os.listdir(script_directory) if f.endswith('requests.py')]
    
    user_info = load_user_info(user_info_path)
    if not user_info:
        print("無法加載用戶信息，程序終止。")
        return
    
    id_to_owner = {user['id']: user['owner'] for user in user_info}
    all_transactions = {}

    for script in scripts:
        script_id = script[:3]
        script_path = os.path.join(script_directory, script)
        print(f"Running {script_path}...")

        output = execute_script(script_path)
        if output is None:
            continue
        
        try:
            transactions = json.loads(output)
        except json.JSONDecodeError as e:
            print(f"解析腳本 {script} 的輸出時出現錯誤: {e}")
            continue
        
        owner = id_to_owner.get(script_id, "未知用戶")
        if len(owner) == 2:
            owner = f"{owner[0]} {owner[1]}"
        
        if owner not in all_transactions:
            all_transactions[owner] = {"transaction": [], "total_amount": 0}
        
        print(f"\nTransactions from {script}:")
        print(json.dumps(transactions, indent=4, ensure_ascii=False))

        if isinstance(transactions, dict) and "交易記錄" in transactions and "總金額" in transactions:
            all_transactions[owner]["total_amount"] += transactions["總金額"]
            for transaction in transactions["交易記錄"]:
                all_transactions[owner]["transaction"].append(transaction)
        else:
            for transaction in transactions:
                all_transactions[owner]["transaction"].append(transaction)
                all_transactions[owner]["total_amount"] += transaction.get("金額", 0)

    utc_now = datetime.utcnow()
    utc_plus_8_now = utc_now + timedelta(hours=8)
    current_month_str = utc_plus_8_now.strftime("%Y-%m")
    output_month_directory = os.path.join(output_base_directory, current_month_str)

    if not os.path.exists(output_month_directory):
        os.makedirs(output_month_directory)

    google_sheets_key = "/Users/chenyaoxuan/Desktop/myproject/MarketProject/astute-harmony-425407-p9-826d675d86f9.json"
    gc = pygsheets.authorize(service_file=google_sheets_key)
    google_sheets_url = "https://docs.google.com/spreadsheets/d/1SGNEuh-FjiBxoxH73NcDELDGbSO71vhc7DbkGuKk4wo/edit#gid=1894821213"
    sheet = gc.open_by_url(google_sheets_url)

    market_data = {}

    for owner, data in all_transactions.items():
        output_rows = []

        for transaction in data["transaction"]:
            output_rows.append([
                owner,
                transaction["時間"][:10] if "時間" in transaction else "",
                transaction["銀行卡"] if "銀行卡" in transaction else "",
                transaction["提款方式"] if "提款方式" in transaction else "",
                transaction["金額"] if "金額" in transaction else "",
                transaction["狀態"] if "狀態" in transaction else ""
            ])
        
        df = pd.DataFrame(output_rows, columns=["編號姓名", "時間", "銀行卡", "提款方式", "金額", "狀態"])
        total_row = pd.DataFrame([["", "", "", "總金額", data["total_amount"], ""]], columns=["編號姓名", "時間", "銀行卡", "提款方式", "金額", "狀態"])
        df = pd.concat([df, total_row], ignore_index=True)

        user_id = next((uid for uid, uname in id_to_owner.items() if uname == owner), "未知ID")
        output_file_name = f'{user_id}_{owner}_{current_month_str}蝦皮提款記錄.xlsx'
        output_file_path = os.path.join(output_month_directory, output_file_name)

        df.to_excel(output_file_path, index=False)
        adjust_excel_format(output_file_path, font_size=20)

        print(f"Transactions for {owner} have been written to {output_file_path}")

        market_data[owner[:7]] = output_rows

    update_google_sheets(market_data, sheet)
    print("所有資料已成功備份到 Google Sheets！")

if __name__ == "__main__":
    main()