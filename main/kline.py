import csv
import json
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = '1VUueCUnGjzMYK4FGNi7wfWKr19I2sjOrcL31nVyNWOSdvYL6WPhVND7CfHWlOSQVEgJ7Ay648nysS04DbsnHQ'
SECRETKEY = 'h8B4G6gVvuz03xNxt9JfxrlQqUbjKX0OFsGsKSms1J1Tw8awuU6aNEYSGHaYUgZpEDG4XGtluOxyVJbyV0UZA'

def k_line():
    payload = {}
    path = '/openApi/swap/v3/quote/klines'
    method = "GET"
    paramsMap = {
        "symbol": "ID-USDT",
        "interval": "1h",
        "limit": "1000",
        "startTime": "1702717199998"
    }
    paramsStr = prase_param(paramsMap)
    response_text = send_request(method, path, paramsStr, payload)
    return json.loads(response_text)

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

def prase_param(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+"&timestamp="+str(int(time.time() * 1000))

if __name__ == '__main__':
    kline_data = k_line()
    print("demo:", kline_data)
