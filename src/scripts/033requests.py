import json
from datetime import datetime
import pytz
import requests

# 033requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=883e4d4d-b8e9-4c3b-bf72-05f52aff469b&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "883e4d4d-b8e9-4c3b-bf72-05f52aff469b",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=883e4d4d-b8e9-4c3b-bf72-05f52aff469b; "
        "_sapid=79908b011c433a67aebc560033dbc0c2ad32c908f53ee61afc5c896e; "
        "_QPWSDCXHZQA=e1bfa5ce-99f2-4192-b9d0-53c9c5bc4782; "
        "REC7iLP4Q=a863ef1d-c82e-4817-9507-a24514858e8f; "
        "SPC_SEC_SI=v1-N25RZGJtOVBhMndHTmVhaRY1Q/XBv15J2+HMs37p+ytpJkzo4I9sYDXOWgQwe3JGA7jgbIUOFOltthXcqpoK76JMqvQyLr/mMt3UuKL27iE=; "
        "SPC_F=MM04rMbMD3emblZtIv18yYie4OLlev9Q; "
        "__stripe_mid=4d47be9c-f49c-499c-ae3c-21d6e54b403f8784c0; "
        "REC_T_ID=eee10bf1-2d24-11ed-a217-2cea7f960266; "
        "SC_DFP=ChkTD4QQRltJRjpqRA7VlAbcnOIgxsim; "
        "_gcl_au=1.1.590781647.1722930451; "
        "SPC_SI=qmWfZgAAAAAyZVRHTjZxZGppzwIAAAAAWEJ5UG9abFg=; "
        "SPC_U=-; "
        "_fbp=fb.1.1722930451355.16377146143206811; "
        "SPC_R_T_ID=Vxxoycdp3ho58gzA2Bn4or+00xAkpxLiv/f1m0ovwppc9znlEv3Q82w4btx8J0TI8x1Eh3a5Qs957zZ5Ehn4VHcJ7Q9+VglAhbJfhrG+CwaJ2hzmPuVA4ukbgHm/FPiCQu+sXJBQwy3ewOet+0h1eA==; "
        "SPC_R_T_IV=bjRlTlF1cjUwbjRQRDFUaA==; "
        "SPC_T_ID=Vxxoycdp3ho58gzA2Bn4or+00xAkpxLiv/f1m0ovwppc9znlEv3Q82w4btx8J0TI8x1Eh3a5Qs957zZ5Ehn4VHcJ7Q9+VglAhbJfhrG+CwaJ2hzmPuVA4ukbgHm/FPiCQu+sXJBQwy3ewOet+0h1eA==; "
        "SPC_T_IV=bjRlTlF1cjUwbjRQRDFUaA==; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_ga=GA1.2.915923675.1722930452; "
        "_gid=GA1.2.365902802.1722930452; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_CLIENTID=TU0wNHJNYk1EM2Vtyllohyjeqyalkiob; "
        "SPC_EC=.YzhJdlVDZ2FqVHgxaTBlTuIZmS+MgeTmoC1/lnjfjuLHFa/at8XH8zp1IZQeaKP1XrDrwARGT1Iu7dgDogyYOvVtllcGTroW87aZG7qQVJZhXpvNvHqKJhf7LkXzDR0L3oUH5H1brLIDs579ANDZIdigVbKFx/UDJRcX2GKbt1Y8cQGdLnaEspAJYd21uOfLhiTCNBJOZ+536rirOrW+Sg==; "
        "SPC_ST=.YzhJdlVDZ2FqVHgxaTBlTuIZmS+MgeTmoC1/lnjfjuLHFa/at8XH8zp1IZQeaKP1XrDrwARGT1Iu7dgDogyYOvVtllcGTroW87aZG7qQVJZhXpvNvHqKJhf7LkXzDR0L3oUH5H1brLIDs579ANDZIdigVbKFx/UDJRcX2GKbt1Y8cQGdLnaEspAJYd21uOfLhiTCNBJOZ+536rirOrW+Sg==; "
        "_ga_E1H7XE0312=GS1.1.1722930452.1.0.1722930469.43.0.0; "
        "SPC_SC_TK=992fff4b60eec0dfdf17e90ee20327ec; "
        "SPC_SC_UD=1309002411; "
        "SPC_SC_SESSION=90b64427245f088bd5c4c8c45002c986_1_1309002411; "
        "SPC_STK=jTomHEMq5gDaFhCrgnYmSGPM0wzY/xrwrBTI+irzOg1Whq6gLsSHqQSDc7MFrZF5ZV/9o7VjmN71OfWn25K6u5fB2btqTg/xqm5XijZn1o8MvYaD/dIGzQBYIR8AcArL1mPaNogurGyN8UHjHuq1GM6APAYWDH4MywNBziJi318zf9AqPBV/dgdSb6lSq7KQfkzG/SNavQ0Xtgk1jLTPLQGPIPp6vUruk9tdUQ3/vYY=; "
        "CTOKEN=LpdoxlPIEe%2B0VOqp%2FkQxYg%3D%3D; "
        "SPC_CDS_CHAT=de51a8b8-f57d-49f2-87e2-f47125952955; "
        "shopee_webUnique_ccd=%2BJTf5mQdSQyXrw08WRE%2FGg%3D%3D%7CCCSBEBeRkfpKKXSwyfJDOiEFkJDoq7C0GXPsVK4fL%2FvGaCPvGI1wjsP%2FYqUdDTZ7gKuHLjQVKbbVZ80%3D%7C3LcXZE4wxmUFBghj%7C08%7C3; "
        "ds=a7bbb1c31863f4be21db81dd9a4f1b64"
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