import json
from datetime import datetime
import pytz
import requests

# 031requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=2700ef03-1938-46ca-b6b6-97da650b618c&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "2700ef03-1938-46ca-b6b6-97da650b618c",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=2700ef03-1938-46ca-b6b6-97da650b618c; "
        "_gcl_au=1.1.1361414007.1722929524; "
        "_fbp=fb.1.1722929524170.909721262800167194; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_gid=GA1.2.1996024401.1722929525; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_F=dnqPCh71iUeSBV36VskEMbjcLrM3od86; "
        "REC_T_ID=b1ef06db-47fa-11ef-b789-a2975eb97a86; "
        "SC_DFP=JKUesrVFLjlaWUETJThFmZeukjYCFcNZ; "
        "SPC_SI=+tCxZgAAAAAyR1BhMnh0dKPfBAAAAAAAQlBPVGF1R3o=; "
        "SPC_U=-; "
        "SPC_R_T_ID=k8c7Se9ZOxFWUe5xYrxBvDdZ95kqwi/IKOn3+a6mR2XSeRv38utDvogPScEr6UxtVwZNxmAq3BbW9zTVRg0KYEQTj9jB55tiQiKvL5zQaN+wpegM4AL54MVKNBCZCA/Xb5156x5cICq9xzZRZskTCpEEPtK5pCI5RFi0vzbpH/s=; "
        "SPC_R_T_IV=UmRUYk9qbGFwUmhiemI2bQ==; "
        "SPC_T_ID=k8c7Se9ZOxFWUe5xYrxBvDdZ95kqwi/IKOn3+a6mR2XSeRv38utDvogPScEr6UxtVwZNxmAq3BbW9zTVRg0KYEQTj9jB55tiQiKvL5zQaN+wpegM4AL54MVKNBCZCA/Xb5156x5cICq9xzZRZskTCpEEPtK5pCI5RFi0vzbpH/s=; "
        "SPC_T_IV=UmRUYk9qbGFwUmhiemI2bQ==; "
        "_ga=GA1.2.2069349202.1722929525; "
        "SPC_EC=.eFVHZG1SZUhkbG0xYk15cCCZwn2Rfe5TlpCmY+qW27DFQmY4RXIZaZN3KvGXTxaE1TePTPVQ/8C2vZEfwN80xGchwo4rs3QP/CJKXU9OFoBOcOm7ZqQgkjwWAYoF27w0yDQ2eFtcClOpvo8fCccgZ6jkLDy5D01jz6T41Jndg6lcPerp1/Y2bR9v+rQD08rV0p601bJ3Ps5nv8e+wumXgw==; "
        "SPC_ST=.eFVHZG1SZUhkbG0xYk15cCCZwn2Rfe5TlpCmY+qW27DFQmY4RXIZaZN3KvGXTxaE1TePTPVQ/8C2vZEfwN80xGchwo4rs3QP/CJKXU9OFoBOcOm7ZqQgkjwWAYoF27w0yDQ2eFtcClOpvo8fCccgZ6jkLDy5D01jz6T41Jndg6lcPerp1/Y2bR9v+rQD08rV0p601bJ3Ps5nv8e+wumXgw==; "
        "SPC_CLIENTID=ZG5xUENoNzFpVWVTgocnalmflybnusoz; "
        "_ga_E1H7XE0312=GS1.1.1722929524.1.1.1722929564.20.0.0; "
        "SPC_SC_TK=f91f83130938e2e34d24e1219e4ec644; "
        "SPC_SC_UD=1305236104; "
        "SPC_SC_SESSION=982eb166af93c3d9a1b9758f28488437_1_1305236104; "
        "SPC_STK=SsBhPY4wAF5AxG8zBNeyjnR/LAvnpqgVbBFK7G6J+ZFOcdLosWQQrvAviU4W/F5vUYsLBDmORW48EX5dYsqkfDtkb3i1a38O/wvXVmNRO84m4gV3AH4e/lOHfvbnAK5QnfanCaH9eFXl0J+fkfFWIS6QPpJCv2qMYEamLeJ+ks5pSsHwQaYFk4jYbdCXHL8rnFWPG4m2lGdPVUWb7Ezu5JaRz0ULNYE9lh/BWEh4t1w=; "
        "SPC_CDS_CHAT=9acfa74b-0239-4f43-9b20-1f9dea6edef0; "
        "CTOKEN=E3bmAlPGEe%2BI%2BSZT14ykEw%3D%3D; "
        "_sapid=2baeedc7b47f5ca1fc8230c64bab27af3253a6e5b39ff86e60583d97; "
        "_QPWSDCXHZQA=407c6f3b-07a7-4577-e6ac-177e3890d2c6; "
        "REC7iLP4Q=478c9c49-ee09-47af-af64-ef9b5cc62c03; "
        "shopee_webUnique_ccd=me6LRaH3XxIBIz9vyoYF6g%3D%3D%7CrEK80HhONJBgIC6he2AKBUjw1wLUlROejDp6Zhs46Hxvnn9i%2FZ25%2ByHGPPLcHhiWDF%2Bmc5UJyZ99cnA%3D%7CRHHzfNuEjnctjAjG%7C08%7C3; "
        "ds=cb5223f14bcb20ac2d7c8ae9b9033f5d; "
        "SPC_SEC_SI=v1-b1lDMFkzUG9nTFVMWUR1V0LbvBvhCDuKHuMMzx/oVN8gby0vX3+WtUZ4RZ+0mzN8ckEuv+uW5mUbUI2j4TfC45fDvrDsxOfskxIYxt/S320="
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