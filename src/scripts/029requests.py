import json
from datetime import datetime
import pytz
import requests

# 029requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=7c919a07-ba11-46ef-be60-cffb45ace344&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "7c919a07-ba11-46ef-be60-cffb45ace344",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "_QPWSDCXHZQA=acdff6ed-b64b-423a-89c7-5c918427850f; "
        "REC7iLP4Q=c45fd217-530d-40e3-a5c6-aa76d55b1c19; "
        "SPC_CDS=7c919a07-ba11-46ef-be60-cffb45ace344; "
        "_sapid=e98c73c58680d9a33ea0aec487d354f4754539fa551405afc5662883; "
        "SPC_SEC_SI=v1-dDM2SjFLbGpQallYWE0xUCF97S7V9SHa8tHiHZRHOVffS6mblcw3OQX8YTsP/yqhWVr7xMx9if9j+JH4Nf6d68+RQM2wBihkL7yCYUvTZF0=; "
        "SPC_F=3tOSgGzv7FyYe5VitLSvgps4t8vslulZ; "
        "REC_T_ID=6e213505-47f8-11ef-91bb-3640e1932620; "
        "SC_DFP=KpWBTKEUaaySDKhXKAAFMOKnwxcFccju; "
        "_gcl_au=1.1.1696623136.1722928576; "
        "SPC_SI=qWWfZgAAAABYSUNsalNxa4wRlAIAAAAAVTVhQWFobmg=; "
        "SPC_U=-; "
        "SPC_R_T_ID=4oq0sRyHMAiJtXFeDWvqa3fstPO88sP28hWOZw7Adyk/PUjd9d/6Ymd5gQt6+fu7328I5Akrpsl6zNZE+AvCvWTc4/MzZXcIbkJOnpHYdrOUw3Zb1MUkD84ODfVApqFl8IebW2mEqwvJ/jqeQHUDJiFZOvOHw9caXDJjzc5T2n0=; "
        "SPC_R_T_IV=ZnZzeGsyY1R3UHRCYWhFSQ==; "
        "SPC_T_ID=4oq0sRyHMAiJtXFeDWvqa3fstPO88sP28hWOZw7Adyk/PUjd9d/6Ymd5gQt6+fu7328I5Akrpsl6zNZE+AvCvWTc4/MzZXcIbkJOnpHYdrOUw3Zb1MUkD84ODfVApqFl8IebW2mEqwvJ/jqeQHUDJiFZOvOHw9caXDJjzc5T2n0=; "
        "SPC_T_IV=ZnZzeGsyY1R3UHRCYWhFSQ==; "
        "_fbp=fb.1.1722928577235.625133748102663327; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_ga=GA1.2.1180246129.1722928578; "
        "_gid=GA1.2.1143638881.1722928578; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_CLIENTID=M3RPU2dHenY3RnlZvzyjozwaaxblsgsr; "
        "SPC_EC=.eUdkMjFORkpTdEFtQWFrVHiJUJCjCgI+uQ40Tb/kdKUBFBASY46hwyXQls8dFKDLW4yyV8inHySu5I8/oydpCKmO7BUKr7MQ/+AKYFUC3q3S/GCTJBUhmDPZHltLkLW+eLa0eSebYfGYpSNyEh5epF8u2mkVygNTmR2F+wOh3i1RpOxhTSWLynGMjJRoN0sv4vtvoqKzSSGMHjiDtf/EpQ==; "
        "SPC_ST=.eUdkMjFORkpTdEFtQWFrVHiJUJCjCgI+uQ40Tb/kdKUBFBASY46hwyXQls8dFKDLW4yyV8inHySu5I8/oydpCKmO7BUKr7MQ/+AKYFUC3q3S/GCTJBUhmDPZHltLkLW+eLa0eSebYfGYpSNyEh5epF8u2mkVygNTmR2F+wOh3i1RpOxhTSWLynGMjJRoN0sv4vtvoqKzSSGMHjiDtf/EpQ==; "
        "_ga_E1H7XE0312=GS1.1.1722928577.1.0.1722928599.38.0.0; "
        "SPC_SC_TK=b3fd2be000041f678e383c4e6e9914e4; "
        "SPC_SC_UD=1305575150; "
        "SPC_SC_SESSION=57bf014103f9f8bd591a303ad9e6bfba_1_1305575150; "
        "SPC_STK=N6E8hIL78TKViuSFp7gvh1kd9Plq2EbeMaDRYQCe6qpiC+hIblX6Rm1+AIIGfpCJIYrSActtanpJiij0BhgBEfKY/zDeotqtlP9mLrsysoXELfil5zLFvnLi4a1HjZRDNG4l29BxrtRvVblo3Aq88BYLTkQUSe1J2yObtlGKvUXpp6uhD8nEUsOIybVCEMCFLyZAgmhq7pR+bnQTk8zQ9CkA9HtmcaJEqHioHKA44II=; "
        "SPC_CDS_CHAT=01005e7f-a475-4f2b-bb60-0513a76ff95a; "
        "shopee_webUnique_ccd=6xCG18HAWEpUUJKfZPlFdg%3D%3D%7CrWKcWf67f3sBgLMO6O2aQ9oT%2FD2yT%2FGIALDnYyl1wlIJxoxqwOCe9Hunjoy4ZwxiBV0e4xhebaw%3D%7C1d90%2FgL%2Fk4pSgU2X%7C08%7C3; "
        "ds=570a71c123e8cca2e1792a4c89f2478d; "
        "CTOKEN=2uWPCVPDEe%2BEK6ocfxp1pQ%3D%3D"
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