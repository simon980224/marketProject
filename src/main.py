from datetime import datetime
import subprocess
import sys
import os
import json
import pandas as pd

def run_script(script_name):
    """運行指定的Python腳本並返回其輸出"""
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    return result.stdout

def load_user_info(user_info_path):
    """從指定的JSON文件加載用戶信息"""
    with open(user_info_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    scripts = ['005requests.py', '027requests.py']
    script_dir = '/Users/chenyaoxuan/Desktop/myproject/marketProject/src/scripts'
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
        
        owner = id_to_owner.get(script_id, "未知用戶")
        
        if owner not in all_transactions:
            all_transactions[owner] = {"date": [], "transaction": []}
        
        if not transactions:  # 檢查是否有交易內容
            print(f'{script} 無交易內容')
            all_transactions[owner]["transaction"].append({"金額": 0, "狀態": "無交易內容", "帳戶": "", "時間": ""})  # 添加一個表示無交易內容的條目
        else:
            print(f"\nTransactions from {script}:")
            print(json.dumps(transactions, indent=4, ensure_ascii=False))
            
            for transaction in transactions:
                all_transactions[owner]["transaction"].append(transaction)

    # 準備輸出到Excel的數據
    max_len = max(len(data["transaction"]) for data in all_transactions.values())
    output_data = {owner: [] for owner in all_transactions}

    for owner, data in all_transactions.items():
        combined_data = []
        for transaction in data["transaction"]:
            combined_data.append(owner)
            combined_data.append(transaction["時間"][:10])  # 使用交易中的時間字段的前10個字符
            combined_data.append(transaction["帳戶"])
            combined_data.append(str(transaction["金額"]))
            combined_data.append(transaction["狀態"])
        # 填充空白以使所有列具有相同的長度
        while len(combined_data) < max_len * 5:
            combined_data.extend([''] * 5)
        output_data[owner] = combined_data

    # 將數據轉換為DataFrame
    df = pd.DataFrame(output_data)

    # 根據當前日期生成輸出檔案名
    today_date_str = datetime.now().strftime("%Y-%m-%d")
    output_file_name = f'{today_date_str}蝦皮自動提款記錄.xlsx'
    output_file_path = os.path.join('/Users/chenyaoxuan/Desktop/', output_file_name)

    # 將DataFrame寫入Excel文件
    df.to_excel(output_file_path, header=False, index=False)

    print(f"All transactions have been written to {output_file_path}")

if __name__ == "__main__":
    main()