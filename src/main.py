from datetime import datetime
import subprocess
import sys
import os
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

def run_script(script_name):
    """運行指定的Python腳本並返回其輸出"""
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"運行腳本 {script_name} 時出現錯誤: {e}")
        return None

def load_user_info(user_info_path):
    """從指定的JSON文件加載用戶信息"""
    try:
        with open(user_info_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"加載用戶信息文件 {user_info_path} 時出現錯誤: {e}")
        return None

def set_font_and_adjust_dimensions(file_path, size=20):
    """設置Excel文件中的字體大小並自動調整列寬和行高"""
    workbook = load_workbook(file_path)
    sheet = workbook.active
    
    for row in sheet.iter_rows():
        for cell in row:
            cell.font = Font(size=size)
    
    # 自動調整列寬
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            if cell.value:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column].width = adjusted_width
    
    # 自動調整行高
    for row in sheet.iter_rows():
        max_height = 0
        for cell in row:
            if cell.value:
                cell_lines = str(cell.value).split('\n')
                cell_height = len(cell_lines) * 20  # 每行字體高度約為20
                if cell_height > max_height:
                    max_height = cell_height
        sheet.row_dimensions[row[0].row].height = max_height
    
    workbook.save(file_path)

def main():
    scripts = ['005requests.py', '027requests.py']
    script_dir = '/Users/chenyaoxuan/Desktop/myproject/marketProject/src/scripts'
    user_info_path = '/Users/chenyaoxuan/Desktop/myproject/marketProject/userInfo.json'
    
    # 讀取用戶資訊
    user_info = load_user_info(user_info_path)
    if not user_info:
        print("無法加載用戶信息，程序終止。")
        return
    
    # 建立從ID到owner的映射
    id_to_owner = {user['id']: user['owner'] for user in user_info}
    
    # 用於存儲所有交易數據的字典
    all_transactions = {}

    for script in scripts:
        script_id = script[:3]  # 假設腳本名的前三個字符是ID
        script_path = os.path.join(script_dir, script)
        print(f"Running {script_path}...")

        output = run_script(script_path)
        if output is None:
            continue
        
        try:
            transactions = json.loads(output)
        except json.JSONDecodeError as e:
            print(f"解析腳本 {script} 的輸出時出現錯誤: {e}")
            continue
        
        owner = id_to_owner.get(script_id, "未知用戶")
        
        if owner not in all_transactions:
            all_transactions[owner] = {"transaction": [], "total_amount": 0}
        
        print(f"\nTransactions from {script}:")
        print(json.dumps(transactions, indent=4, ensure_ascii=False))

        # 如果transactions是包含總金額和交易記錄的字典
        if isinstance(transactions, dict) and "交易記錄" in transactions and "總金額" in transactions:
            all_transactions[owner]["total_amount"] += transactions["總金額"]
            for transaction in transactions["交易記錄"]:
                all_transactions[owner]["transaction"].append(transaction)
        else:
            for transaction in transactions:
                all_transactions[owner]["transaction"].append(transaction)
                all_transactions[owner]["total_amount"] += transaction.get("金額", 0)

    # 根據當前日期生成輸出檔案名
    today_date_str = datetime.now().strftime("%Y-%m-%d")

    for owner, data in all_transactions.items():
        output_rows = []

        for transaction in data["transaction"]:
            output_rows.append([
                owner,
                transaction["時間"][:10] if "時間" in transaction else "",
                transaction["銀行卡"] if "銀行卡" in transaction else "",
                transaction["金額"] if "金額" in transaction else "",
                transaction["狀態"] if "狀態" in transaction else ""
            ])
        
        # 將數據轉換為DataFrame
        df = pd.DataFrame(output_rows, columns=["法人", "時間", "銀行卡", "金額", "狀態"])

        # 在DataFrame的最後一行添加總金額
        total_row = pd.DataFrame([["", "", "總金額", data["total_amount"], ""]], columns=["法人", "時間", "銀行卡", "金額", "狀態"])
        df = pd.concat([df, total_row], ignore_index=True)

        # 為每個擁有者生成單獨的Excel文件名
        output_file_name = f'{today_date_str}_{owner}_蝦皮自動提款記錄.xlsx'
        output_file_path = os.path.join('/Users/chenyaoxuan/Desktop/', output_file_name)

        # 將DataFrame寫入Excel文件
        df.to_excel(output_file_path, index=False)

        # 設置Excel文件中的字體大小並自動調整列寬和行高
        set_font_and_adjust_dimensions(output_file_path, size=20)

        print(f"Transactions for {owner} have been written to {output_file_path}")

if __name__ == "__main__":
    main()