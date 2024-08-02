import requests

url = "https://seller.shopee.tw/api/v4/seller/local_wallet/get_withdrawal_options"
params = {
    "SPC_CDS": "ae5c11c6-24e2-4130-9299-742f1576e7e5",
    "SPC_CDS_VER": "2"
}
headers = {
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

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    json_data = response.json()
    
    # 提取銀行名和銀行帳號末四碼
    bank_accounts = json_data['data']['bank_accounts']
    
    for account in bank_accounts:
        bank_name = account['bank_name']
        account_number = account['account_number']
        print(f"銀行名: {bank_name}, 銀行帳號末四碼: {account_number[-4:]}")
else:
    print(f"請求失敗，狀態碼: {response.status_code}")