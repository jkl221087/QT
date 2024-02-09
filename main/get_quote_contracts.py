import time
import csv
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = '1VUueCUnGjzMYK4FGNi7wfWKr19I2sjOrcL31nVyNWOSdvYL6WPhVND7CfHWlOSQVEgJ7Ay648nysS04DbsnHQ'
SECRETKEY = 'h8B4G6gVvuz03xNxt9JfxrlQqUbjKX0OFsGsKSms1J1Tw8awuU6aNEYSGHaYUgZpEDG4XGtluOxyVJbyV0UZA'

#取得報價合約
def get_quote_contracts():
    path = '/openApi/swap/v2/quote/contracts'
    method = "GET"
    paramsMap = {}
    paramsStr = parse_param(paramsMap)
    return send_request(method, path, paramsStr)

#取得簽名
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    return signature

#發送請求
def send_request(method, path, params_str):
    url = f"{APIURL}{path}?{params_str}&signature={get_sign(SECRETKEY, params_str)}"
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers)
    return response.json()# 返回 JSON 格式數據

#解析參數
def parse_param(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr + "&timestamp=" + str(int(time.time() * 1000))

#寫入CSV檔案
def write_to_csv(data, filename):
    with open (filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())  # 使用 DictWriter 將字典寫入 CSV 文件
        writer.writeheader()  # 寫入列標題
        writer.writerow(data)  # 寫入數據

#執行主def
if __name__ == '__main__':
    contracts_data = get_quote_contracts()
    print("Quote Contracts:", get_quote_contracts())
    write_to_csv(contracts_data, 'contracts_data.csv')  # 將數據寫入 CSV 文件
