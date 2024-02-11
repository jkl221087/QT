# 导入所需的库和函数
from Latest_Funding import Latest_funding
import json
from get_trading import get_trading  # 导入你的 get_trading 函数
from depth_information import depth_information
from kline import k_line
import time

def sentiment_based_strategy():
    # 获取最新的资金数据
    funding_data = Latest_funding()
    funding_info = json.loads(funding_data)['data']

    # 获取深度信息
    depth_info = depth_information()

    # 获取K线数据
    kline_data = k_line()

    # 这里获取到了多空持仓人数比和资金费率，你需要根据实际情况获取该数据
    long_short_ratio = 0.9816 # 多空持仓人数比
    funding_rate = float(funding_info['lastFundingRate'])  # 资金费率

    # 根据市场动态计算停止价格
    stop_price = calculate_stop_price(depth_info)

    # 执行量价分析
    volume_price_analysis(depth_info, kline_data)

    # 根据多空持仓人数比和资金费率进行交易决策
    if long_short_ratio > 1 and funding_rate > 0:
        print("Market sentiment: Bullish")
        # 在此执行买入操作
        trading_response = get_trading("ID-USDT", "BUY", "LONG", "MARKET", 10000, "")  # 或者移除takeProfit参数
        print("Trading response:", trading_response)
    elif long_short_ratio < 1 and funding_rate < 0:
        print("Market sentiment: Bearish")
        # 在此执行卖出或持仓调整操作
        trading_response = get_trading("ID-USDT", "SELL", "SHORT", "MARKET", 10000, "")  # 或者移除takeProfit参数
        print("Trading response:", trading_response)
    else:
        print("Market sentiment: Neutral", )
        # 在此执行持仓调整或待机操作



# 计算停止价格的函数
def calculate_stop_price(depth_info):
    # 获取卖单价格列表中的第一个元素（价格）
    lowest_ask_price = min(depth_info['data']['asks'], key=lambda x: float(x[0]))[0]
    stop_price = float(lowest_ask_price) * 1.01  # 将停止价格设置为当前最低卖单价格的1%高于
    return stop_price

# 量价分析函数
#{'open': '0.2766', 'close': '0.2825', 'high': '0.2854', 'low': '0.2766', 'volume': '1765554.00', 'time': 1702724400000}
def volume_price_analysis(depth_info, k_line):
    print("Performing volume-price analysis...")
    
    # 从深度信息中获取卖单价格列表
    asks_prices = [float(ask[0]) for ask in depth_info['data']['asks']]
    
    # 从 K 线数据中获取成交量和价格
    for kline_point in k_line['data']:
        kline_volume = float(kline_point['volume'])
        kline_open = float(kline_point['open'])
        kline_close = float(kline_point['close'])
        kline_high = float(kline_point['high'])
        kline_low = float(kline_point['low'])
        
        # 计算移动平均线
        historical_prices = [float(point['close']) for point in k_line['data']]
        moving_average = sum(historical_prices) / len(historical_prices)
        
        # 比较当前价格与移动平均线的关系
        if kline_close > moving_average:
            print("Price above the moving average, bullish")
        elif kline_close < moving_average:
            print("Price below the moving average, bearish")
        else:
            print("Price equals the moving average, neutral")
        
        # 分析价格趋势的强度
        price_change = kline_close - kline_open
        if abs(price_change) > (kline_high - kline_low) * 0.5:
            print("Strong price movement detected")
        else:
            print("Weak price movement detected")
    
    # 你可以继续根据需要添加更多的量价分析逻辑


# 在主程序中调用交易策略函数
if __name__ == "__main__":
    while True:
        sentiment_based_strategy()
        # 每次运行策略后暂停一段时间，避免频繁请求接口
        time.sleep(10)  # 暂停60秒
