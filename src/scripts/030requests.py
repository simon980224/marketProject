import json
from datetime import datetime
import pytz
import requests

# 030requests.py

# 常數
URL_WALLET = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2?SPC_CDS=f8eb9c91-d46c-490c-bb5c-28ee835f919f&SPC_CDS_VER=2"
URL_BANK = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
PARAMS = {
    "SPC_CDS": "f8eb9c91-d46c-490c-bb5c-28ee835f919f",
    "SPC_CDS_VER": "2"
}
HEADERS = {
    "content-type": "application/json;charset=UTF-8",
    "cookie": (
        "SPC_CDS=f8eb9c91-d46c-490c-bb5c-28ee835f919f; "
        "SPC_F=qHG5659gn4UwQTO1f75htKCVJy8GSGQM; "
        "SPC_CDS_CHAT=e0de8b23-7396-48dd-abbe-48cb49917bf0; "
        "_fbp=fb.1.1721632212446.31572244299209822; "
        "_gcl_au=1.1.678768041.1721632210; "
        "REC_T_ID=705c4c82-47f9-11ef-80e0-6ede63472c9a; "
        "SPC_CLIENTID=cUhHNTY1OWduNFV3npfidivfovajnfsq; "
        "SPC_SI=pmWfZgAAAABkZTU5Zjg2csoCrwIAAAAARUpDNWdVcmU=; "
        "SPC_U=-; "
        "SPC_T_ID=b3VVKtYCtfpDKecodKbuBdG4kL6N5/3hyjapyjk7DUzAT9nmJbd/KrDWnxzLVHEfmrwu0OcnoV26AunR5ad8BR+mbwAVdf6y1Ggtb8b+wahOpuHrdHD0XnJ01ogB28BqmsVHo4KBjjsb0rMAJLL/JMbawQp/tllYFPlW+ENYTFI=; "
        "SPC_T_IV=T2V2S0JnUEVwWHFoaTJTUA==; "
        "SPC_R_T_ID=b3VVKtYCtfpDKecodKbuBdG4kL6N5/3hyjapyjk7DUzAT9nmJbd/KrDWnxzLVHEfmrwu0OcnoV26AunR5ad8BR+mbwAVdf6y1Ggtb8b+wahOpuHrdHD0XnJ01ogB28BqmsVHo4KBjjsb0rMAJLL/JMbawQp/tllYFPlW+ENYTFI=; "
        "SPC_R_T_IV=T2V2S0JnUEVwWHFoaTJTUA==; "
        "AMP_TOKEN=%24NOT_FOUND; "
        "_ga=GA1.2.328200700.1721632214; "
        "_gid=GA1.2.175121108.1722929271; "
        "_dc_gtm_UA-61915057-6=1; "
        "SPC_EC=.UG1JTEdrTnVVSEdqTDVIY1a41VEPz7JBZW+nJtOf2sFnqdhtqf9TB1V/+G1ygUWlF6DjXwHGe7d/izRNgp339AT/fZuBynIoBi3dRkUvDCM1K9JsTesf6BnTGxMMM1iBAmco6ggqNjV7/t0+6w8J1U1IDvy7kB0fean7ia5i/y+Grf+DIT/FIdiTykkjgXajFCTURGWWhz81iieBNctPTw==; "
        "SPC_ST=.UG1JTEdrTnVVSEdqTDVIY1a41VEPz7JBZW+nJtOf2sFnqdhtqf9TB1V/+G1ygUWlF6DjXwHGe7d/izRNgp339AT/fZuBynIoBi3dRkUvDCM1K9JsTesf6BnTGxMMM1iBAmco6ggqNjV7/t0+6w8J1U1IDvy7kB0fean7ia5i/y+Grf+DIT/FIdiTykkjgXajFCTURGWWhz81iieBNctPTw==; "
        "_ga_E1H7XE0312=GS1.1.1722929269.2.1.1722929292.37.0.0; "
        "SPC_SC_TK=66b224e9958afad2b36ea14dd958b94e; "
        "SPC_SC_UD=1302013844; "
        "SPC_SC_SESSION=6ee92f0edcf2cb53d70445ae30f43a8e_1_1302013844; "
        "SPC_STK=Sb9XzCqE1p6DXIJxRtrHr4EcCyCq8CMliW1BWm50wtR4wx8qruhHf4RQcGMHlrnicRXCigUZGnMYVjNsh7Sb4LbjafVTwcuOibzpcPrg/HDLXV8vtJD4+eKyEhgwt0/kbZ17K+ePetZB6g3nc489EHgRtX2jbrjzV3qh6To1q3BSabd1KHA7E5fs8srSthixqFHOY6Pd9H3VSXA0eRApfCWD2PLSGcPiotViTwBvBKc=; "
        "SC_DFP=MqWTTMPUZqFQiWVLbzzHMGSHVVSaiSwv; "
        "CTOKEN=cLJzQ1PFEe%2BMjoY0ACOaWg%3D%3D; "
        "_sapid=835c7e9f0c8ccff95470a39eefe7a941faf0385300098aec61a5f718; "
        "_QPWSDCXHZQA=e049f59a-192c-4804-cd29-9aebfa9ea74b; "
        "REC7iLP4Q=d43a84c8-30f4-4a7a-98b6-115eb2057f97; "
        "shopee_webUnique_ccd=dbJtZzbLhsVVyzGh0kWLZA%3D%3D%7COB0lQwluKE2T%2F2zSAUDa96HMko9jwtNGAi8XN%2B9AIAeNSAnHfTRnhbwPdKsYhdIyzjej43qRDWweeJA%3D%7CjVjozb2seriXoOv3%7C08%7C3; "
        "ds=fa2aaf5d9b83621be8811ec0b7e8b3ef; "
        "SPC_SEC_SI=v1-TFNKcjczbFJpOGZWZ25xOXUojBLfUxb2Tdduo3no+kXmTiQAkwFvG4vVGT0VqS3r4clwCm8Ri/E31/yUfishwkfFKXVqWKfmeXSHTitQKKw="
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