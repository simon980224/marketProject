from datetime import datetime
import subprocess
import sys
import os
import json
import pandas as pd

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
            all_transactions[owner] = {"transaction": []}
        
        if not transactions:  # 檢查是否有交易內容
            print(f'{script} 無交易內容')
            all_transactions[owner]["transaction"].append({"金額": 0, "狀態": "無交易內容", "帳戶": "", "時間": ""})
        else:
            print(f"\nTransactions from {script}:")
            print(json.dumps(transactions, indent=4, ensure_ascii=False))
            
            for transaction in transactions:
                all_transactions[owner]["transaction"].append(transaction)

    # 根據當前日期生成輸出檔案名
    today_date_str = datetime.now().strftime("%Y-%m-%d")

    for owner, data in all_transactions.items():
        output_rows = []

        for transaction in data["transaction"]:
            output_rows.append([
                owner,
                transaction["時間"][:10] if "時間" in transaction else "",
                transaction["帳戶"] if "帳戶" in transaction else "",
                transaction["金額"] if "金額" in transaction else "",
                transaction["狀態"] if "狀態" in transaction else ""
            ])
        
        # 將數據轉換為DataFrame
        df = pd.DataFrame(output_rows, columns=["法人", "時間", "帳戶", "金額", "狀態"])

        # 為每個擁有者生成單獨的Excel文件名
        output_file_name = f'{today_date_str}_{owner}_蝦皮自動提款記錄.xlsx'
        output_file_path = os.path.join('/Users/chenyaoxuan/Desktop/', output_file_name)

        # 將DataFrame寫入Excel文件
        df.to_excel(output_file_path, index=False)

        print(f"Transactions for {owner} have been written to {output_file_path}")

if __name__ == "__main__":
    main()