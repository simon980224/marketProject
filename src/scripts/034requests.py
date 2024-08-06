import json
from datetime import datetime
import pytz
import requests

# 034requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=de078ee2-1dad-4462-9e94-2e603e36ca69&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "de078ee2-1dad-4462-9e94-2e603e36ca69",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=de078ee2-1dad-4462-9e94-2e603e36ca69; "
        "_gcl_au=1.1.28303972.1722930670; "
        "_fbp=fb.1.1722930670150.25263460433445063; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_gid=GA1.2.2071986591.1722930671; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_F=MM04rMbMD3emblZtIv18yYie4OLlev9Q; "
        "__stripe_mid=4d47be9c-f49c-499c-ae3c-21d6e54b403f8784c0; "
        "REC_T_ID=eee10bf1-2d24-11ed-a217-2cea7f960266; "
        "SC_DFP=ChkTD4QQRltJRjpqRA7VlAbcnOIgxsim; "
        "SPC_SI=qWWfZgAAAABiNDlpVFVrejHvzQIAAAAASzVIOWhJOWc=; "
        "SPC_CLIENTID=TU0wNHJNYk1EM2Vtwziqnhoqfyxxzwcw; "
        "SPC_U=-; "
        "SPC_SC_SA_TK=; "
        "SPC_SC_SA_UD=; "
        "SPC_SC_OFFLINE_TOKEN=; "
        "SC_SSO=-; "
        "SC_SSO_U=-; "
        "SPC_R_T_ID=VDV/d67HLZtJxdRIZG7QoP8EyzXLqOCh6IlDDC19v2WLBtUgaUTkeMyIfHgLOvWoCEtkiiwYKAG7i7mb6S7ZhiQMsMwoUYP/rudkD2rqvs7bc3pg1+PEg5P/lK2PyM+KkZ2mDc1pTEybAiUAHlY7ng==; "
        "SPC_R_T_IV=SXUzaExDczhmSXVwZW5oWQ==; "
        "SPC_T_ID=VDV/d67HLZtJxdRIZG7QoP8EyzXLqOCh6IlDDC19v2WLBtUgaUTkeMyIfHgLOvWoCEtkiiwYKAG7i7mb6S7ZhiQMsMwoUYP/rudkD2rqvs7bc3pg1+PEg5P/lK2PyM+KkZ2mDc1pTEybAiUAHlY7ng==; "
        "SPC_T_IV=SXUzaExDczhmSXVwZW5oWQ==; "
        "_ga=GA1.1.98509577.1722930671; "
        "SPC_EC=.dEgzSTNQTXVENU1yd1RBZaV9HVqCOI+m609rKwm8aTJEQebgeB3ezGMHhKmf3sNiSE5xfDlJfc9opVCppX6U+frmApioXIaICeOYGiQffqqtAosSDaQhC/dnRqaqXQ38cZelS3Wtr1Eu6IXuoj7ttaN0LJ8qN5vHEMezFLiVWF1revXoqi8+nmaN4t0VISwddNwsZflUrEgo8JJRQf0Gaw==; "
        "SPC_ST=.dEgzSTNQTXVENU1yd1RBZaV9HVqCOI+m609rKwm8aTJEQebgeB3ezGMHhKmf3sNiSE5xfDlJfc9opVCppX6U+frmApioXIaICeOYGiQffqqtAosSDaQhC/dnRqaqXQ38cZelS3Wtr1Eu6IXuoj7ttaN0LJ8qN5vHEMezFLiVWF1revXoqi8+nmaN4t0VISwddNwsZflUrEgo8JJRQf0Gaw==; "
        "_ga_E1H7XE0312=GS1.1.1722930670.1.1.1722930715.15.0.0; "
        "SPC_SC_TK=3162c652397276925ea70c76ddd72ebd; "
        "SPC_SC_UD=4404976; "
        "SPC_SC_SESSION=ddbedb1dc946230a049f7c1475a41c16_1_4404976; "
        "SPC_STK=+VYD7i+WTrAdj2NrrjtgojERKAMp36AR1UXlvtKhl+nGni6q+Q6PmH32p2jthkT0I9WdxqjpcdtWqmDEGhmuai9y7QAeEW1kdAcFc7hBwGn1QfbRYOhyonze+DMZtSHjT+vHv7X8leoP6XC0+Ceit0y/beusRye+nM9uBnRNW2zkxfJ5G6lF5unIHp+gI46iu+4oKbM9BEYntsqv2azM6A==; "
        "CTOKEN=wRDAq1PIEe%2BZUMpaiO64hg%3D%3D; "
        "SPC_CDS_CHAT=bfd4e4d9-172b-4b6a-b753-23df92d781fd; "
        "_sapid=17df5de80909ec8ec0f380e9bbdb57e640ca1a5bb1c4b86b8b54f1c2; "
        "_QPWSDCXHZQA=4d88a5d7-9c97-4c40-b3ae-957f7b148272; "
        "REC7iLP4Q=8760adf3-8635-4f64-bbcc-ead4929467af; "
        "shopee_webUnique_ccd=RyYSKg0YL93CdjrB0X%2Bxjg%3D%3D%7CqoZnPz%2FCXeD4xGDRluGI2HIBjtKPGEGsb8TzJum0CWTXqEF7Ph7UUwMZoHbqvyHT%2B5KrxVCcsceoTfY%3D%7C%2BfeVKPbEVe0UHdOZ%7C08%7C3; "
        "ds=36e251d5ae2a0f0747ab55193d3f7c12; "
        "SPC_SEC_SI=v1-cjVqSjBwcml5d3pGOVJqZQP+P5nfBJDE1N9wvHq6TD5ELkHPETRRBElub05mWfWI+jRIfeWNtsqeYTauP9Wl1UxkOudnSZ6edAMtH4BbMvg="
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