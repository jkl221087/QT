# 导入所需的库和函数
import json
import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY = '1VUueCUnGjzMYK4FGNi7wfWKr19I2sjOrcL31nVyNWOSdvYL6WPhVND7CfHWlOSQVEgJ7Ay648nysS04DbsnHQ'
SECRETKEY = 'h8B4G6gVvuz03xNxt9JfxrlQqUbjKX0OFsGsKSms1J1Tw8awuU6aNEYSGHaYUgZpEDG4XGtluOxyVJbyV0UZA'

# 获取深度信息
def depth_information():
    payload = {}
    path = '/openApi/swap/v2/quote/depth'
    method = "GET"
    paramsMap = {
        "symbol": "ID-USDT",
        "limit": "5"
    }
    paramsStr = parse_param(paramsMap)
    response = send_request(method, path, paramsStr, payload)
    return json.loads(response)

# 获取签名
def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    return signature

# 发送请求
def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

# 解析参数
def parse_param(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    return paramsStr+"&timestamp="+str(int(time.time() * 1000))

# 执行主函数
if __name__ == '__main__':
    depth_info = depth_information()
    print("Depth information:", depth_info)

    # 提取深度信息中的买单和卖单数据
    bids = depth_info['data']['bids']
    asks = depth_info['data']['asks']
    
    print("Bids:", bids)
    print("Asks:", asks)
