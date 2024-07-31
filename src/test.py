import requests

# 創建一個會話對象
session = requests.Session()

# 設置Cookie
cookies = {
    "SPC_T_ID": "uOETBMe6PRrDy+X/SD34tEDw14zrWVjwQGvaPeu7P2sGGHyNEvR+uxiiOveSxmkCOWldq9h6DPAK+OmdNq+hESOc7xTqYGiimpvfuiyggFAN9tniMItxnZB4OiAdA8UfwmZVzem4M06Gnf6pndQx/cV4k9YVbb87P/+6DzGA40I=",
    "SPC_F": "ZQgMuiYzKcj6bgypg95NHCZKhZVweS4F",
    "SPC_SC_SESSION": "5a127150c64abcb62c99bf4edb0ca45d_1_187791978",
    "SPC_R_T_ID": "uOETBMe6PRrDy+X/SD34tEDw14zrWVjwQGvaPeu7P2sGGHyNEvR+uxiiOveSxmkCOWldq9h6DPAK+OmdNq+hESOc7xTqYGiimpvfuiyggFAN9tniMItxnZB4OiAdA8UfwmZVzem4M06Gnf6pndQx/cV4k9YVbb87P/+6DzGA40I=",
    "SPC_SC_UD": "187791978",
    "SPC_SI": "IsCQZgAAAABIOGZVYVZKdtP7BAAAAAAAN2h3ZnBtNkU=",
    "SPC_SC_TK": "f91f639467930f075a14a4d21e77c6b3",
    "SPC_EC": ".Q1VXd0lKUTI4djg2cTZ4Zg8iS6VeyfYNHaAOEvc8kKpQnC2SlxQHFU6I06JXOIzo4xm70r/6yt+/eOVV4NtRqRgjQO+8UjxFz8QyU8nhj+Loj/1UXXe5xv7RJqwuOknVzhB92uBsCWPtnnsRQk3AdmmDB6SkM4YmPRl6dCIRXhOeaDFITuGMLdY0sstgY7xEfxqXiVAmCcBjX3M0hA/KMw==",
    "__stripe_mid": "f5771447-f04c-4e6d-8522-193593f8a6a772ee0c",
    "CTOKEN": "NFAWwkirEe%2BPxML8AO35mA%3D%3D",
    "REC_T_ID": "e470ee55-27ac-11ee-a033-089204a3b46f",
    "SC_DFP": "EDDPxkwquMnbBKgrxTTRuYhrDvCsDLAI",
    "SPC_R_T_IV": "YTR1bjVnWGk5UEhYYmRNSw==",
    "SPC_SEC_SI": "v1-TGE4Q2U0ZUtpYnJlR2JxccpwPfn40FQVB1T2t8RdXNB02VOLFXHhFZuJwCwCqC2X3Ym7mGUBK1FKuPrQCUUKxnJrHkYLvUpXLryrqXqaXvo=",
    "SPC_ST": ".Q1VXd0lKUTI4djg2cTZ4Zg8iS6VeyfYNHaAOEvc8kKpQnC2SlxQHFU6I06JXOIzo4xm70r/6yt+/eOVV4NtRqRgjQO+8UjxFz8QyU8nhj+Loj/1UXXe5xv7RJqwuOknVzhB92uBsCWPtnnsRQk3AdmmDB6SkM4YmPRl6dCIRXhOeaDFITuGMLdY0sstgY7xEfxqXiVAmCcBjX3M0hA/KMw==",
    "SPC_STK": "5hOThSGoBSkURM4WFrndXr0MgdxdsHGoXotNbyfEWBoEwsNtwr16VIFHA0tcm/IKZm3VHerk8Dd2All37fRiynBTSAN8ZLbXyTUGkr17REnz8DC8HC49MmPS9Hh3PwOgPxIhQFnKWfjUXvMprSwZoY69FR+OAmZd7PNEB3BZGAbU/FurWTvgxpseYJIXvnE+m1EF9tw3PYjuajMr+uTBogOnbLG07epJDKjoUsnyCQg=",
    "SPC_T_IV": "YTR1bjVnWGk5UEhYYmRNSw==",
    "SPC_U": "187791978"
}

# 將Cookie添加到會話中
session.cookies.update(cookies)

# 發送GET請求
response = session.get("https://shopee.tw")

# 打印響應狀態碼和內容
print(response.status_code)
print(response.text)