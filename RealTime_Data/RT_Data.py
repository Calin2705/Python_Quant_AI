import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
import time

mt.initialize()

login = 51685762
password = 'o38M@eNWSJ8BS3'
server = "ICMarketsSC-Demo"
mt.login(login, password, server)

symbol = 'GBPUSD'
timeframe = mt.TIMEFRAME_M1
date_from = datetime(2024, 3, 11)
date_to = datetime.now()

for i in range(10):
    prices = pd.DataFrame(mt.copy_rates_range(symbol, timeframe, date_from, date_to))
    prices['time'] = pd.to_datetime(prices['time'], unit='s')
    print(prices[-3:])
    time.sleep(60)
