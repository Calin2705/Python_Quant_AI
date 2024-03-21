import MetaTrader5 as mt5

mt5.initialize()
login = 51685762
password = 'o38M@eNWSJ8BS3'
server = "ICMarketsSC-Demo"
mt5.login(login, password, server)



# symbol = 'EURUSD'
volume = 0.1
action = mt5.TRADE_ACTION_DEAL
order_type = mt5.ORDER_TYPE_BUY

stop_loss = 1.0  # set to 0.0 if you don't want SL
take_profit = 1.2  # set to 0.0 if you don't want TP

def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid

request = {
    "action": action,
    "symbol": 'EURUSD',
    "volume": 0.1,  # float
    "type": mt5.ORDER_TYPE_BUY,
    "price": get_market_price('EURUSD', 0),
    "sl": stop_loss,  # float
    "tp": take_profit,  # float
    "deviation": 20,
    "magic": 0,
    "comment": "python market order",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
}

res = mt5.order_send(request)




# close position

positions = mt5.positions_get()
print('open positions', positions)

# Working with 1st position in the list and closing it
pos1 = positions[0]

def reverse_type(type):
    # to close a buy positions, you must perform a sell position and vice versa
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.ORDER_TYPE_SELL
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.ORDER_TYPE_BUY


def get_close_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).bid
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "position": pos1.ticket,
    "symbol": pos1.symbol,
    "volume": pos1.volume,
    "type": reverse_type(pos1.type),
    "price":get_close_price(pos1.symbol, pos1.type),
    "deviation": 20,
    "magic": 0,
    "comment": "python close order",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
}

res = mt5.order_send(request)
