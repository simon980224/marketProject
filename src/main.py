import subprocess
import sys
import os
import json
from datetime import datetime
import pandas as pd

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    return result.stdout

def load_user_info(user_info_path):
    with open(user_info_path, 'r', encoding='utf-8') as file:
        return json.load(file)

if __name__ == "__main__":
    scripts = ['005requests.py', '027requests.py']
    script_dir = '/Users/chenyaoxuan/Desktop/myproject/marketProject/src/'
    user_info_path = '/Users/chenyaoxuan/Desktop/myproject/marketProject/userInfo.json'
    
    # 讀取用戶資訊
    user_info = load_user_info(user_info_path)
    
    # 建立從ID到owner的映射
    id_to_owner = {user['id']: user['owner'] for user in user_info}
    
    # 用於存儲所有交易數據的字典
    all_transactions = {}

    for script in scripts:
        script_id = script[:3]  # 假設腳本名的前三個字符是ID
        script_path = os.path.join(script_dir, script)
        print(f"Running {script_path}...")
        output = run_script(script_path)
        
        transactions = json.loads(output)
        
        if not transactions:  # 檢查是否有交易內容
            today_date = datetime.now().strftime("%Y-%m-%d")
            print(f'{today_date} {script} 無交易內容')
        else:
            print(f"\nTransactions from {script}:")
            print(json.dumps(transactions, indent=4, ensure_ascii=False))
        
        owner = id_to_owner.get(script_id, "未知用戶")
        if owner not in all_transactions:
            all_transactions[owner] = {"date": [], "transaction": []}
        
        for transaction in transactions:
            all_transactions[owner]["date"].append(datetime.now().strftime("%Y-%m-%d"))
            all_transactions[owner]["transaction"].append(transaction)

    # 準備輸出到Excel的數據
    max_len = max(len(data["date"]) for data in all_transactions.values())
    output_data = {owner: [] for owner in all_transactions}

    for owner, data in all_transactions.items():
        combined_data = []
        for date, transaction in zip(data["date"], data["transaction"]):
            combined_data.append(owner)
            combined_data.append(transaction["時間"])
            combined_data.append(transaction["金額"])
            combined_data.append(transaction["狀態"])
        # 填充空白以使所有列具有相同的長度
        combined_data.extend([''] * (max_len * 4 - len(combined_data)))
        output_data[owner] = combined_data

    # 將數據轉換為DataFrame
    df = pd.DataFrame(output_data)

    # 將DataFrame寫入Excel文件
    output_file = '/Users/chenyaoxuan/Desktop/all_transactions.xlsx'
    df.to_excel(output_file, header=False, index=False)

    print(f"All transactions have been written to {output_file}")