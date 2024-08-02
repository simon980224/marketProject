import requests
import json
from datetime import datetime

def fetch_transactions_and_bank_info():
    url_wallet = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2"
    url_bank = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
    params = {
        "SPC_CDS": "ae5c11c6-24e2-4130-9299-742f1576e7e5",
        "SPC_CDS_VER": "2"
    }
    headers = {
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

    # 固定7月1日00:00:00.000到7月31日23:59:59.999的時間範圍
    start_time = datetime(2024, 7, 1, 0, 0, 0, 0)
    end_time = datetime(2024, 7, 31, 23, 59, 59, 999000)

    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    data_wallet = {
        "wallet_type": 0,
        "pagination": {"limit": 20},
        "start_time": start_timestamp,
        "end_time": end_timestamp,
        "transaction_types": []
    }

    try:
        # 首先請求錢包交易記錄
        response_wallet = requests.post(url_wallet, params=params, headers=headers, data=json.dumps(data_wallet))
        response_wallet.raise_for_status()  # 如果狀態碼不是200，這行會拋出HTTPError

        # 然後請求銀行信息
        response_bank = requests.get(url_bank, headers=headers, params=params)
        response_bank.raise_for_status()  # 如果狀態碼不是200，這行會拋出HTTPError
    except requests.exceptions.HTTPError as http_err:
        if response_wallet.status_code == 403 or response_bank.status_code == 403:
            print("403 Forbidden - 請重新取得憑證。")
        else:
            print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Other error occurred: {err}")
        return []

    # 處理錢包交易記錄的響應
    response_data_wallet = response_wallet.json()

    # 狀態轉換函數
    def translate_status(status):
        status_dict = {
            2: "進行中",
            3: "已完成"
        }
        return status_dict.get(status, "未知狀態")

    # 處理銀行信息的響應
    response_data_bank = response_bank.json()

    # 提取銀行名和銀行帳號末四碼
    bank_accounts = response_data_bank['data']['bank_accounts']
    bank_info = {
        account['bank_account_id']: {
            "銀行名": account['bank_name'],
            "銀行帳號末四碼": account['account_number'][-4:]
        }
        for account in bank_accounts
    }

    # 過濾只顯示"自動提款"的交易記錄，並關聯銀行信息
    auto_withdraw_transactions = [
        {
            "時間": datetime.utcfromtimestamp(txn['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
            "金額": txn['amount'],
            "狀態": translate_status(txn['status']),
            "帳戶": bank_info[txn['bank_details']['bank_account_id']]['銀行名'] + bank_info[txn['bank_details']['bank_account_id']]['銀行帳號末四碼'] if 'bank_details' in txn and 'bank_account_id' in txn['bank_details'] and txn['bank_details']['bank_account_id'] in bank_info else "未知"
        }
        for txn in response_data_wallet['data']['transactions'] if txn['transaction_type'] == 4000
    ]

    # 計算總金額
    total_amount = sum(txn["金額"] for txn in auto_withdraw_transactions)
    
    # 將總金額添加到結果最上層
    result = {
        "總金額": total_amount,
        "交易記錄": auto_withdraw_transactions
    }

    # 按時間排序
    result["交易記錄"] = sorted(result["交易記錄"], key=lambda x: datetime.strptime(x["時間"], '%Y-%m-%d %H:%M:%S'))

    return result

if __name__ == "__main__":
    transactions = fetch_transactions_and_bank_info()
    print(json.dumps(transactions, indent=4, ensure_ascii=False))