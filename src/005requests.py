import requests
import json
from datetime import datetime

url = "https://seller.shopee.tw/api/v3/finance/get_wallet_transactions_v2"
params = {
    "SPC_CDS": "eb690bef-8b46-4e98-8126-f3178df2b58f",
    "SPC_CDS_VER": "2"
}

headers = {
    "authority": "seller.shopee.tw",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json;charset=UTF-8",
    "cookie": ("_gcl_au=1.1.2115538007.1722406374; _gid=GA1.2.931038229.1722406374; _fbp=fb.1.1722406374465.770437716310844772; "
               "SPC_F=74f5H76QUQK6Ha5RDlM4cfRMsHW8inm1; REC_T_ID=42926ffe-fdfe-11ee-8acc-c28dae5ad99c; SC_DFP=xRQCqZQkfoWsYuFRZpchCEbJlBzRXNNc; "
               "SPC_SI=qWWfZgAAAABvOFJHUmNwSqRR5gAAAAAAcEh0a0UxMjE=; SPC_CLIENTID=NzRmNUg3NlFVUUs2efyvmqmhjgltfhjh; SPC_EC=.Z2hscEtnNm04T092OVpoMJkZyvKo6Ef566oBvdJfOWa1MwfgBzUFO5X6wY0gvQ5oXVQc6dSAAUWKCcNPiFLNMoOhSxvkJ+ArTTqDk5hLghn3BO7bgs3S5+oaUbZ6p+g+D6d6hc9Z251VZCEyLSft3+3w5K6cWlPsaKM/1pTcboNzqiYla1YeZGBtYbfAqFZzDilZVdxPhMEHUdqvkjfKfw==; "
               "SPC_ST=.Z2hscEtnNm04T092OVpoMJkZyvKo6Ef566oBvdJfOWa1MwfgBzUFO5X6wY0gvQ5oXVQc6dSAAUWKCcNPiFLNMoOhSxvkJ+ArTTqDk5hLghn3BO7bgs3S5+oaUbZ6p+g+D6d6hc9Z251VZCEyLSft3+3w5K6cWlPsaKM/1pTcboNzqiYla1YeZGBtYbfAqFZzDilZVdxPhMEHUdqvkjfKfw==; "
               "SPC_SC_TK=f15a0c48fd413a8bff77ad9dbf544056; SPC_SC_UD=1237726476; SPC_SC_SESSION=c3eaf927df300311945588c9206c8ccc_1_1237726476; "
               "SPC_STK=BxrHuTgjMUvUSyygRBLKULehSaXwdC3uPbD0firaOjXQ6J/Y+D7LdhZ9Caq1Y3y8CplpcdBPkMpZ0iGdjz2gHV3QREI6Hn9oUDSNMPbSEKvZPn0p9M7BBceBfMvgBHfHTqCUrLUmbJziI/Pm9io3Mgh5BeXIOjMZVQi4YcPtrmeINFNvwYS7SBdHOxTDj5siPmLp3YXRcjs4ON/8iZKSFnVQ7GHhbisNABbeBlQsHY4=; "
               "SPC_U=1237726476; SPC_SEC_SI=v1-S01rSG5WQllyN3g4dmtxWXBrersFrxggWZnGSOWLMvLV/0y6t2Edi4ncHeluQwm5vPMuMnVRwP7jHl0pLIYfPSF8Zatoi6/Kcqm/VRpZNs8=; "
               "_QPWSDCXHZQA=bd137f25-2600-45ce-e8ad-034096d5cf56; REC7iLP4Q=03325c7b-4dff-4df7-bf89-7ca26bbe4ded; SPC_R_T_IV=RlVYM2lSbEVaVjlBcGM5Zw==; "
               "SPC_T_ID=8/aXVk30hoquNDaMX5wknYSi5UM4MbXslkVf0uBYeXKgVAkTzhae/ZWY8MAWnVWVuM51XQ8EQk32ogXs94BoOvz+8V/6S74zxv0SPDigbQWquGklXy/k+wSnM92w7Tfb5YYrDnirHKZB/yaCOq5rynfMd7BmF0yWZUmSKUdqY/E=; SPC_T_IV=RlVYM2lSbEVaVjlBcGM5Zw==; SPC_R_T_ID=8/aXVk30hoquNDaMX5wknYSi5UM4MbXslkVf0uBYeXKgVAkTzhae/ZWY8MAWnVWVuM51XQ8EQk32ogXs94BoOvz+8V/6S74zxv0SPDigbQWquGklXy/k+wSnM92w7Tfb5YYrDnirHKZB/yaCOq5rynfMd7BmF0yWZUmSKUdqY/E=; "
               "AMP_TOKEN=%24NOT_FOUND; _dc_gtm_UA-61915057-6=1; _ga=GA1.1.2056944256.1722406374; SPC_CDS=eb690bef-8b46-4e98-8126-f3178df2b58f; SPC_CDS_CHAT=b5378025-98d6-4db8-8f81-315ffb9dfe5e; "
               "_sapid=aa3aad6adfee040c7d16706b475f40777b31e4ce2316d46ef2d8fd95; _ga_E1H7XE0312=GS1.1.1722405723.2.1.1722408276.56.0.0; CTOKEN=c5StlU8IEe%2BMxe6Mtr%2BqWA%3D%3D; shopee_webUnique_ccd=LwgePQdja5UczryQmVbEvA%3D%3D%7CrJnoybiahOFDO7SU55SGa%2B8f3U%2Bzf4pro80%2F%2Fpu7FgZV83vu%2BfQJEYQf57zm6GSZWK52MUzHyJ%2Bq8mQ%3D%7CxOxgP5q4hO6g8R3p%7C08%7C3; ds=ba63a6907cc1c267faf9005fa344ac87"),
    "origin": "https://seller.shopee.tw",
    "priority": "u=1, i",
    "referer": "https://seller.shopee.tw/portal/finance/wallet/shopeepay",
    "sc-fe-session": "89F1B2020B9EDF90",
    "sc-fe-ver": "21.58321",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

data = {
    "wallet_type": 0,
    "pagination": {"limit": 20},
    "start_time": 1719763200,
    "end_time": 1722441599,
    "transaction_types": []
}

response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
response_data = response.json()

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
        "金額": txn['amount'],
        "狀態": translate_status(txn['status'])
    }
    for txn in response_data['data']['transactions'] if txn['transaction_type'] == 4000
]

# 打印過濾後的結果
for txn in auto_withdraw_transactions:
    print(json.dumps(txn, indent=4, ensure_ascii=False))