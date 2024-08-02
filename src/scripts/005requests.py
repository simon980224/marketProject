import requests
import json
from datetime import datetime

def fetch_transactions():
    url = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2"
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

    data = {
        "wallet_type": 0,
        "pagination": {"limit": 20},
        "start_time": start_timestamp,
        "end_time": end_timestamp,
        "transaction_types": []
    }

    try:
        response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果狀態碼不是200，這行會拋出HTTPError
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            print("403 Forbidden - 請重新取得憑證。")
        else:
            print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Other error occurred: {err}")
        return []

    response_data = response.json()
    print(response_data)

    # 狀態轉換函數
    def translate_status(status):
        status_dict = {
            2: "進行中",
            3: "已完成"
        }
        return status_dict.get(status, "未知狀態")

    # 過濾只顯示"自動提款"的交易記錄
    auto_withdraw_transactions = [
        {
            "時間": datetime.utcfromtimestamp(txn['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
            "金額": str(txn['amount']),
            "狀態": translate_status(txn['status']),
            "帳戶": txn['bank_details']['bank_account_id'] if 'bank_details' in txn and 'bank_account_id' in txn['bank_details'] else "未知"
        }
        for txn in response_data['data']['transactions'] if txn['transaction_type'] == 4000
    ]

    return auto_withdraw_transactions

if __name__ == "__main__":
    transactions = fetch_transactions()
    print(json.dumps(transactions, indent=4, ensure_ascii=False))