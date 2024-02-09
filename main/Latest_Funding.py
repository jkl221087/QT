import csv
import json
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = '1VUueCUnGjzMYK4FGNi7wfWKr19I2sjOrcL31nVyNWOSdvYL6WPhVND7CfHWlOSQVEgJ7Ay648nysS04DbsnHQ'
SECRETKEY = 'h8B4G6gVvuz03xNxt9JfxrlQqUbjKX0OFsGsKSms1J1Tw8awuU6aNEYSGHaYUgZpEDG4XGtluOxyVJbyV0UZA'

def Latest_funding():
    payload = {}
    path = '/openApi/swap/v2/quote/premiumIndex'
    method = "GET"
    paramsMap = {
        "symbol": "ID-USDT"
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    return signature

def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+"&timestamp="+str(int(time.time() * 1000))

def write_to_csv(data):
    with open('Latest_Funding.csv', 'w', newline='') as csvfile:
        fieldnames = ['symbol', 'markPrice', 'indexPrice', 'lastFundingRate', 'nextFundingTime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'symbol': data['symbol'],
            'markPrice': data['markPrice'],
            'indexPrice': data['indexPrice'],
            'lastFundingRate': data['lastFundingRate'],
            'nextFundingTime': data['nextFundingTime']
        })

if __name__ == '__main__':
    print("funding", Latest_funding())