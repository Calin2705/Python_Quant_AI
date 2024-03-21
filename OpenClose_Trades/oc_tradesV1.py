import MetaTrader5 as mt5

mt5.initialize()
login = 51685762
password = 'o38M@eNWSJ8BS3'
server = "ICMarketsSC-Demo"
mt5.login(login, password, server)


symbol = "USDJPY"
symbol_info = mt5.symbol_info(symbol)
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
sl = 0
tp = 0

def open_trade_buy(symbol, lot, price, sl ,tp, deviation):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


mt5.order_send(open_trade_buy(symbol,lot,price,sl,tp,deviation))
