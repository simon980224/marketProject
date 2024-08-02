import json
from datetime import datetime

import pytz
import requests

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=25f9045f-8c37-4326-b535-acbe00978586&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "ae5c11c6-24e2-4130-9299-742f1576e7e5",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=ae5c11c6-24e2-4130-9299-742f1576e7e5; "
        "SPC_F=74f5H76QUQK6Ha5RDlM4cfRMsHW8inm1; "
        "REC_T_ID=42926ffe-fdfe-11ee-8acc-c28dae5ad99c; "
        "SC_DFP=xRQCqZQkfoWsYuFRZpchCEbJlBzRXNNc; "
        "_gcl_au=1.1.2091290950.1722414505; "
        "_gid=GA1.2.846147447.1722414505; "
        "SPC_SI=r2WfZgAAAABvMHBCYUNkbs2/6QAAAAAAaGYxZnhERVM=; "
        "SPC_U=-; "
        "_fbp=fb.1.1722414505348.181564866909928500; "
        "SPC_T_IV=WFFHODdIdjM1YWJaR1JNUw==; "
        "SPC_R_T_ID=cK/hkS0SFdIRdErQJZ2Nx+KAvu94OPJVowuKDKVNbLGiw3Z6ja3Q/RCfT4ZSWel4Npq7xpsLNaI8a6WxuavPlMpoAERgEgjdK1K8iWosqX2q/peTZccNqi7QMNhHcfNvp3NmcYSG5Ns65YG/uK700RTS2uKKGAZeLvTJIbXkcdU=; "
        "SPC_R_T_IV=WFFHODdIdjM1YWJaR1JNUw==; "
        "SPC_T_ID=cK/hkS0SFdIRdErQJZ2Nx+KAvu94OPJVowuKDKVNbLGiw3Z6ja3Q/RCfT4ZSWel4Npq7xpsLNaI8a6WxuavPlMpoAERgEgjdK1K8iWosqX2q/peTZccNqi7QMNhHcfNvp3NmcYSG5Ns65YG/uK700RTS2uKKGAZeLvTJIbXkcdU=; "
        "_ga=GA1.1.984738795.1722414505; "
        "SPC_CLIENTID=NzRmNUg3NlFVUUs2zvrnzutqktcxwijg; "
        "SPC_EC=.azNyaTVQSk5sT2VHSHlkNfKevrg1hykuxb9r5wNYhQZF4MPzzb2zg+XwGKmC39LdSNSzEo3QWOR5i5d5jCTdxnXvycrDpmFSn1Hy/pkVrVk4rTDDayTg3sJwR9lKIjmIRJJjCJy0f5HNIhcHxyCT5Pa7IxjkS4J9VGO/DnwZtLBVRlNnGUmZ7BBedtsxAcM2bcwZZO8RzJiMXRjXLgD0Yg==; "
        "SPC_ST=.azNyaTVQSk5sT2VHSHlkNfKevrg1hykuxb9r5wNYhQZF4MPzzb2zg+XwGKmC39LdSNSzEo3QWOR5i5d5jCTdxnXvycrDpmFSn1Hy/pkVrVk4rTDDayTg3sJwR9lKIjmIRJJjCJy0f5HNIhcHxyCT5Pa7IxjkS4J9VGO/DnwZtLBVRlNnGUmZ7BBedtsxAcM2bcwZZO8RzJiMXRjXLgD0Yg==; "
        "_ga_E1H7XE0312=GS1.1.1722414001.1.1.1722414519.45.0.0; "
        "SPC_SC_TK=f6383a462fce62caf0470936d02f9ed1; "
        "SPC_SC_UD=1237726476; "
        "SPC_SC_SESSION=9d131ac4a4b522b07b21a6b0fef866e5_1_1237726476; "
        "SPC_STK=0UNFsOD6Y+NBPlPFJRLYGID1PY9D25aOhtWQPccYNcRK1sLl+dxemQQBVdmoAsSv6X3sA6UKf5EAlbpS4u8i2i2x65iwvQOeum4OVbEmLWwftigQhRe1jG1EUG4ExjjdmynvHnPmh8kj0NtGMBiD+R0RT4dzSebIv+iFIsu6rpqDFYMVx+F86ijGpU8mLhsK1VWmbBB19M3gbpkh0qalA9qxmKqlGbxvoATey2YC/zA=; "
        "SPC_SEC_SI=v1-NVRJUUJLTU44MVJrdk1JU0tba6GHMQ3jyAW5WqQ0n4/mUglbEwmzvMv/OWZaf2+FvUa0h+R7Bm4ZSurOexRBEibOSrge6ni2wT08IDyTCtI="
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
            "銀行卡": bank_info.get(txn['bank_details']['bank_account_id'], {}).get('銀行名', '未知') + bank_info.get(txn['bank_details']['bank_account_id'], {}).get('銀行帳號末四碼', '未知') if 'bank_details' in txn and 'bank_account_id' in txn['bank_details'] else "未知",
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