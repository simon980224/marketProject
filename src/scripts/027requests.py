import json
from datetime import datetime
import pytz
import requests

# 027requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=25f9045f-8c37-4326-b535-acbe00978586&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "a17130a2-1c3d-4cd5-8cd0-675b598e3601",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_SEC_SI=v1-S01rSG5WQllyN3g4dmtxWXBrersFrxggWZnGSOWLMvLV/0y6t2Edi4ncHeluQwm5vPMuMnVRwP7jHl0pLIYfPSF8Zatoi6/Kcqm/VRpZNs8=; "
        "_QPWSDCXHZQA=bd137f25-2600-45ce-e8ad-034096d5cf56; "
        "REC7iLP4Q=03325c7b-4dff-4df7-bf89-7ca26bbe4ded; "
        "SPC_CDS=a17130a2-1c3d-4cd5-8cd0-675b598e3601; "
        "SPC_F=ZQgMuiYzKcj6bgypg95NHCZKhZVweS4F; "
        "__stripe_mid=f5771447-f04c-4e6d-8522-193593f8a6a772ee0c; "
        "REC_T_ID=e470ee55-27ac-11ee-a033-089204a3b46f; "
        "SC_DFP=EDDPxkwquMnbBKgrxTTRuYhrDvCsDLAI; "
        "_gcl_au=1.1.2045440076.1722410382; "
        "_fbp=fb.1.1722410382503.804605928463130251; "
        "SPC_SI=r2WfZgAAAABvMHBCYUNkblcp6AAAAAAARmUxSlZWNUo=; "
        "SPC_U=-; "
        "SPC_R_T_ID=D6dfuPPjEY2AqeopBYA5XNb7PHPK4H78ngvwOMZ5yMLwz2GHEQ0etoKz7HvBhyfZheP5VEfYGMV4pUCYQzFr1oAJqTRjByFWTFq3eOdrG5bZKTLaazv/7Xm+FNM/cyBo0sX+u8ACCNGK1dGsTukG/V6e1luHI5XDk5kZ37SGqwY=; "
        "SPC_R_T_IV=YU45b2pqR3hqVjdmcHpjYg==; "
        "SPC_T_ID=D6dfuPPjEY2AqeopBYA5XNb7PHPK4H78ngvwOMZ5yMLwz2GHEQ0etoKz7HvBhyfZheP5VEfYGMV4pUCYQzFr1oAJqTRjByFWTFq3eOdrG5bZKTLaazv/7Xm+FNM/cyBo0sX+u8ACCNGK1dGsTukG/V6e1luHI5XDk5kZ37SGqwY=; "
        "SPC_T_IV=YU45b2pqR3hqVjdmcHpjYg==; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_ga=GA1.2.1778247764.1722410383; "
        "_gid=GA1.2.1440178138.1722410383; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_CLIENTID=WlFnTXVpWXpLY2o2oamebxmizpddvfmu; "
        "SPC_EC=.QzBORWQ4RG9WZDJEdW9NN1qjNA5gIur/Ol9/WSkc44DB+z9aPtlIsafN89rG9kOH3AzrN1BjKIFfbKGIl/nhQs3NWkn8O41TxBGeThg0YO8XhIbpD5hOEINLmOYg8a/vjnYjCWgtS5Zb0aNnfAPj0fOtY4+otOdyYfRyweqLwH2MY2J35SDyGjalrCunKOlCrm8wYrZ0lsspn0m4hivVOQ==; "
        "SPC_ST=.QzBORWQ4RG9WZDJEdW9NN1qjNA5gIur/Ol9/WSkc44DB+z9aPtlIsafN89rG9kOH3AzrN1BjKIFfbKGIl/nhQs3NWkn8O41TxBGeThg0YO8XhIbpD5hOEINLmOYg8a/vjnYjCWgtS5Zb0aNnfAPj0fOtY4+otOdyYfRyweqLwH2MY2J35SDyGjalrCunKOlCrm8wYrZ0lsspn0m4hivVOQ==; "
        "_ga_E1H7XE0312=GS1.1.1722410383.1.0.1722410403.40.0.0; "
        "SPC_SC_TK=ed12d852fa7217250fad054e96e4054d; "
        "SPC_SC_UD=187791978; "
        "SPC_SC_SESSION=f8856583a07e7bc49c54f99ae6a21438_1_187791978; "
        "SPC_STK=K6JbxU7BHvzrogQYa8rI68n/MYlpjgLJvbdRsFXvaps0+jYZGqStcfbsDlp/iORdW5I8L+gkMq3TQDf31ejkdw9cozECXV829FZhliaMxUmq+zau/z1ptN2EvpPSFqs35fN/jDmUpWgtzEqRnhvcxQDog+2riStd3Q9Djm2fUmUWEpsnsyqVnxuILwr+ttdOCcxB9yMXWnZpRhwU7M1ibERgDRrAqZzf8FDYgVtU0Xw=; "
        "SPC_CDS_CHAT=a2f64ee5-e64e-4de1-b5bf-6fa58a025bd4; "
        "CTOKEN=TsLu%2B08NEe%2Bwnr7Dw2%2BXgQ%3D%3D; "
        "_sapid=aa3aad6adfee040c7d16706b475f40777b31e4ce2316d46ef2d8fd95; "
        "shopee_webUnique_ccd=JNn38YP1PfyywtSPj2J24w%3D%3D%7CopnoybiahOFDO7SU55SGa%2B8f3U%2Bzf4pro80%2F%2FpCQNgZV83vu%2BfQJEYQf57zm6GSZWK52MUzHyJ%2Bq8mQ%3D%7CxOxgP5q4hO6g8R3p%7C08%7C3; "
        "ds=abf8459c9a5c7b6b4535594712de77a6"
    ),
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# TODO: 記得改回每月的時間範圍
START_TIME = datetime(2024, 5, 1, 0, 0, 0, 0)
END_TIME = datetime(2024, 7, 31, 23, 59, 59, 999000)

START_TIMESTAMP = int(START_TIME.timestamp())
END_TIMESTAMP = int(END_TIME.timestamp())

DATA_WALLET = {
    "wallet_type": 0,
    "pagination": {"limit": 20},
    "start_time": START_TIMESTAMP,
    "end_time": END_TIMESTAMP,
    "transaction_types": [4000, 4001, 201, 203]
}

# 時區
UTC = pytz.utc
GMT_PLUS_8 = pytz.timezone('Asia/Taipei')

def translate_status(status):
    """狀態轉換函數"""
    status_dict = {
        2: "進行中",
        3: "已完成"
    }
    return status_dict.get(status, "未知狀態")

def fetch_data(url, method="get", data=None):
    """通用的請求函數"""
    try:
        if method == "post":
            response = requests.post(url, params=PARAMS, headers=HEADERS, data=json.dumps(data))
        else:
            response = requests.get(url, headers=HEADERS, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def extract_bank_info(data):
    """提取銀行信息"""
    bank_accounts = data.get('data', {}).get('bank_accounts', [])
    return {
        account['bank_account_id']: {
            "銀行名": account['bank_name'],
            "銀行帳號末四碼": account['account_number'][-4:]
        }
        for account in bank_accounts
    }

def process_transactions(transactions, bank_info):
    """過濾和處理交易記錄"""
    auto_withdraw_transactions = [
        {
            "時間": datetime.fromtimestamp(txn['created_at'], UTC).astimezone(GMT_PLUS_8).strftime('%Y-%m-%d %H:%M:%S'),
            "銀行卡": bank_info.get(txn['bank_details']['bank_account_id'], {}).get('銀行名', '未知銀行') + bank_info.get(txn['bank_details']['bank_account_id'], {}).get('銀行帳號末四碼', '0000') if 'bank_details' in txn and 'bank_account_id' in txn['bank_details'] else "未知",
            "提款方式": "自動提款",
            "金額": txn['amount'],
            "狀態": translate_status(txn['status']),
        }
        for txn in transactions
    ]
    return auto_withdraw_transactions

def fetch_transactions_and_bank_info():
    """主函數：獲取交易記錄和銀行信息"""
    response_data_wallet = fetch_data(URL_WALLET, method="post", data=DATA_WALLET)
    response_data_bank = fetch_data(URL_BANK)

    if not response_data_wallet or not response_data_bank:
        return []

    bank_info = extract_bank_info(response_data_bank)
    transactions = process_transactions(response_data_wallet['data']['transactions'], bank_info)

    total_amount = sum(txn["金額"] for txn in transactions)
    result = {
        "總金額": total_amount,
        "交易記錄": sorted(transactions, key=lambda x: datetime.strptime(x["時間"], '%Y-%m-%d %H:%M:%S'))
    }
    return result

if __name__ == "__main__":
    transactions = fetch_transactions_and_bank_info()
    print(json.dumps(transactions, indent=4, ensure_ascii=False))