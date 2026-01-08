from hyperliquid.utils import constants
import json
import time
import pandas as pd
from utils import setup, klines, market_order, market_close
import ta

address, info, exchange = setup(base_url=constants.MAINNET_API_URL, skip_ws=True)
print(exchange.set_referrer("GUNTHER"))

# getting candles
# kl = klines(info, 'HYPE', '5m', 200)
# print(kl)

# open and close market orders
# market_order(exchange, 'HYPE', False, 0.5)
# market_close(exchange, 'HYPE')

#ema strategy
def ema(coin, timeframe, period1, period2):
    kl = klines(info, coin, timeframe=timeframe, interval=500)
    ema1 = ta.trend.ema_indicator(kl.Close, window = period1)
    ema2 = ta.trend.ema_indicator(kl.Close, window = period2)
    if ema2.iloc[-2] < ema1.iloc[-2] and ema2.iloc[-1] > ema1.iloc[-1]:
        return True
    if ema2.iloc[-2] > ema1.iloc[-2] and ema2.iloc[-1] < ema1.iloc[-1]:
        return False

coin = 'ZEC'
timeframe = '1m'

# changing leverage
print(exchange.update_leverage(10, coin))

while True:
    signal = ema(coin, timeframe, period1=20, period2=5)
    if signal is not None:
        print(signal)
        market_order(exchange, coin, signal, 0.5)
        break
    print('wait 30s')
    time.sleep(30)