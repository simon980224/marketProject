import json
from datetime import datetime
import pytz
import requests

# 032requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=5677d3c1-c559-42f5-8ae7-f288ed95ba90&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "5677d3c1-c559-42f5-8ae7-f288ed95ba90",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=5677d3c1-c559-42f5-8ae7-f288ed95ba90; "
        "_gcl_au=1.1.673989750.1722929732; "
        "_fbp=fb.1.1722929732432.671547013809817299; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_gid=GA1.2.1190442947.1722929733; "
        "SPC_F=g1mv9eSz5Q9636KZjT6Yer9qhbMLDRQA; "
        "REC_T_ID=c740bf55-481e-11ef-a964-3696e98cc054; "
        "SC_DFP=vtYktBalKUsMJPzFUleCCgilmjkWcNrU; "
        "SPC_SI=+tCxZgAAAAB2dnhTOFlvdYNMDQAAAAAAUWFDbXI0MEc=; "
        "SPC_U=-; "
        "SPC_R_T_ID=/GfaKYDiz+DLlK455uTyNXWiHYwDgsGYES41Qx0WU8+ITDUhvspY3XeWv1iyW+4vOg1fWo+1KMjphTHNdRcSgULm/rxN+M7LkIimegIaosuBQeSIt7QUfv5NvMPUBaBqdLDThxiVGKjVgCSkMjZthg==; "
        "SPC_R_T_IV=ODhhdDc0cFBDbnNvY3BZeQ==; "
        "SPC_T_ID=/GfaKYDiz+DLlK455uTyNXWiHYwDgsGYES41Qx0WU8+ITDUhvspY3XeWv1iyW+4vOg1fWo+1KMjphTHNdRcSgULm/rxN+M7LkIimegIaosuBQeSIt7QUfv5NvMPUBaBqdLDThxiVGKjVgCSkMjZthg==; "
        "SPC_T_IV=ODhhdDc0cFBDbnNvY3BZeQ==; "
        "_ga=GA1.2.947488514.1722929733; "
        "SPC_CLIENTID=ZzFtdjllU3o1UTk2rjiqyjpyiggkddks; "
        "SPC_EC=.aUduOG5ZWjdPQ1ZvOWhZN7IoTHDnjF1uPX4vA/UseUWqTB+0bMj9HyEF4IDjSS/DtoeVP47h6GZAwAr+tRc67ObGfx6xRbYpG5iXIqvrqlUBA6bLk8qIx5gs8c0GVxWVl079eo+cjiBxgeZ2IbRHC08COLt8p2uI4PUw7/RBXjBxttHhXAp+T35TusHRYtTGKasGdik1xDMYiq37pa9x2w==; "
        "SPC_ST=.aUduOG5ZWjdPQ1ZvOWhZN7IoTHDnjF1uPX4vA/UseUWqTB+0bMj9HyEF4IDjSS/DtoeVP47h6GZAwAr+tRc67ObGfx6xRbYpG5iXIqvrqlUBA6bLk8qIx5gs8c0GVxWVl079eo+cjiBxgeZ2IbRHC08COLt8p2uI4PUw7/RBXjBxttHhXAp+T35TusHRYtTGKasGdik1xDMYiq37pa9x2w==; "
        "_dc_gtm_UA-61915057-6=1; "
        "_ga_E1H7XE0312=GS1.1.1722929732.1.1.1722929794.60.0.0; "
        "SPC_SC_TK=52e161455004fc5d7dbc25d9fbbde95d; "
        "SPC_SC_UD=1312332058; "
        "SPC_SC_SESSION=9ff6121ff802b5b8a2c5c9193ab3aaab_1_1312332058; "
        "SPC_STK=tfsamCn2BvZRnBigcvRlF/PhI9UZjZiytYQ/xrtbGUcXm/iqorAw73Th3eEp7kEVW5yl/JpjF0JOLx+ebMKcBuejd2Mf6X3fO4uoelE7bq1RgZ3dS6K7P3isI5p82jMZL6EXPyXPOXyz1cq/DKEOtHzCjPnXdLulFyEsA9NhB2fteRmB1RSGekbBQaNnrdoZr8cW2TosSBwT98Qsc/CchJhGkdHYzjRW8tvXlDysHsw=; "
        "CTOKEN=nDfqOFPGEe%2BlR1rRFQnfHg%3D%3D; "
        "SPC_CDS_CHAT=937e5cc0-80f6-4092-a6e4-ed28030cd8fe; "
        "_sapid=48d9b16ecd0b00089ff56c6f4275036c6c5ef9c8c581fa02c46af347; "
        "_QPWSDCXHZQA=b42c76d1-b248-4d6d-80f4-8e20f8f2263a; "
        "REC7iLP4Q=79373ab3-0ca8-455d-a8aa-0230085db360; "
        "shopee_webUnique_ccd=0qg4%2BGtC0Qn1WNyypH6AlA%3D%3D%7Ccbkavpx1YtAqFND2Je8v3vPKovNdPV0eoqK3jCot%2FNwaTPvzz6SziqveLv3g75O81lMhF89U2068oEc%3D%7Cb8KxsEoWUEZOZHRx%7C08%7C3; "
        "ds=a86a1dc803fd5e68d00981eaa8cdb727; "
        "SPC_SEC_SI=v1-Q2FNcU16aGExbm5mcUJ4cEGFe/OW9A5ugrla2ta9jTNgjhlV5iPzRE6r3c7vf0nrzzMqvL+q2l+F0h1cIXx6M99YP1XmRKhp5oZsxHrxzHk="
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