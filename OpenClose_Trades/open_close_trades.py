import MetaTrader5 as mt5


mt5.initialize()
login = 51685762
password = 'o38M@eNWSJ8BS3'
server = "ICMarketsSC-Demo"

mt5.login(login, password, server)


request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "EURUSD",
    "volume": 0.01, # FLOAT
    "type": mt5.ORDER_TYPE_BUY,
    "price": mt5.symbol_info_tick("EURUSD").ask,
    "sl": 0.0, # FLOAT
    "tp": 0.0, # FLOAT
    "deviation": 20, # INTERGER
    "magic": 234000, # INTERGER
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

# order = mt5.order_send(request)
# print(order)



request_close = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "EURUSD",
    "price": mt5.symbol_info_tick("EURUSD").bid,
    "type": mt5.ORDER_TYPE_SELL,
    "volume": 0.01,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    "comment": "python script close",
    # "position": mt5.positions_get()[0]._asdict()['ticket'], # select the position you want to close

}


for i in range(10):
    order = mt5.order_send(request)
    print(order)

ticker = 'BTCUSD'
symbol = 'BTCUSD'
lots = 0.01
buy_order = mt5.ORDER_TYPE_BUY
sell_order = mt5.ORDER_TYPE_SELL
buy_price = mt5.symbol_info_tick(symbol).ask
sell_price = mt5.symbol_info_tick(symbol).bid
def create_orders():
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "price": mt5.symbol_info_tick("EURUSD").bid,
        "type": mt5.ORDER_TYPE_SELL,
        "volume": 0.01,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "comment": "python script close",

    }