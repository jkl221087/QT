import csv
import json
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = '1VUueCUnGjzMYK4FGNi7wfWKr19I2sjOrcL31nVyNWOSdvYL6WPhVND7CfHWlOSQVEgJ7Ay648nysS04DbsnHQ'
SECRETKEY = 'h8B4G6gVvuz03xNxt9JfxrlQqUbjKX0OFsGsKSms1J1Tw8awuU6aNEYSGHaYUgZpEDG4XGtluOxyVJbyV0UZA'


def Recent_transactions():
    payload = {}
    path = '/openApi/swap/v2/quote/trades'
    method = "GET"
    paramsMap = {
    "symbol": "ID-USDT",
    "limit": 10
}
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def praseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+"&timestamp="+str(int(time.time() * 1000))


if __name__ == '__main__':  
    transactions = Recent_transactions()
    print("Recent transactions:",  transactions)


    # 將深度信息寫入 CSV 文件
    Recent_data = json.loads(transactions)
    with open('transactions.csv', 'w', newline='') as csvfile:
        fieldnames = ['time', 'isBuyerMaker', 'price', 'qty', 'QuoteQty', 'fillId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for transaction in Recent_data['data']:
            writer.writerow({
                'time': transaction['time'],
                'isBuyerMaker': transaction['isBuyerMaker'],
                'price': transaction['price'],
                'qty': transaction['qty'],
                'QuoteQty': transaction['quoteQty'],
                'fillId': transaction['fillId']
            })

    print("Depth information has been written to transactions.csv")