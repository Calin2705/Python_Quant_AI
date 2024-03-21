import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
from datetime import datetime


login = 51685762
password = 'o38M@eNWSJ8BS3'
server = "ICMarketsSC-Demo"
mt5.login(login, password, server)


def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid

while True:
    if mt5.initialize():
        symbol = 'XAUUSD'
        timeframe = mt5.TIMEFRAME_M15
        date_from = datetime(2024, 3, 10)
        date_to = datetime.now()
        data = pd.DataFrame(mt5.copy_rates_range(symbol, timeframe, date_from, date_to))
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data = data.iloc[:, :-3]
        data.dropna(inplace=True)

        target_variable = 'close'
        target = data[target_variable]

        scaler = MinMaxScaler(feature_range=(0, 1))
        target_scaled = scaler.fit_transform(target.values.reshape(-1, 1))

        sequence_length = 5  # Adjust this according to your preference
        X, y = create_sequences(target_scaled, sequence_length)

        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
        model.add(Dense(1))  # Output layer with one neuron
        model.compile(optimizer='adam', loss='mean_squared_error')

        history = model.fit(X, y, epochs=100, batch_size=10, callbacks=[keras.callbacks.History()]) #history callbacks added

        last_sequence = target_scaled[-sequence_length:].reshape(1, sequence_length, 1)
        predicted_value = model.predict(last_sequence)
        predicted_value = scaler.inverse_transform(predicted_value)[0][0]

        last_close = data['close'].iloc[-1]

        print("Predicted value:", predicted_value)
        print("Last close value:", last_close)
        print(data[-2:])

        if last_close < predicted_value:
            # if last_close < predicted_value add condition if position open sell or position null
            # sell and position close at first oposit postion
            # (if lstm detect buy when sell close)
            volume = 0.1
            action = mt5.TRADE_ACTION_DEAL
            order_type = mt5.ORDER_TYPE_BUY

            stop_loss = 0.0  # set to 0.0 if you don't want SL
            take_profit = 0.0  # set to 0.0 if you don't want TP


            request = {
                "action": action,
                "symbol": symbol,
                "volume": 0.1,  # float
                "type": mt5.ORDER_TYPE_BUY,
                "price": get_market_price(symbol, 0),
                "sl": stop_loss,  # float
                "tp": take_profit,  # float
                "deviation": 20,
                "magic": 0,
                "comment": "python market order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
            }

            res = mt5.order_send(request)
        elif last_close > predicted_value:
            volume = 0.1
            action = mt5.TRADE_ACTION_DEAL
            order_type = mt5.ORDER_TYPE_SELL

            stop_loss = 0.0  # set to 0.0 if you don't want SL
            take_profit = 0.0  # set to 0.0 if you don't want TP

            request = {
                "action": action,
                "symbol": symbol,
                "volume": 0.1,  # float
                "type": mt5.ORDER_TYPE_SELL,
                "price": get_market_price(symbol, 0),
                "sl": stop_loss,  # float
                "tp": take_profit,  # float
                "deviation": 20,
                "magic": 0,
                "comment": "python market order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
            }

            res = mt5.order_send(request)

        training_loss = history.history['loss']
        epochs = range(1, len(training_loss) + 1)

        plt.plot(epochs, training_loss, 'b', label='Training loss')
        plt.title('Training Loss over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
        time.sleep(5)
    else:
        print("Failed to initialize MetaTrader 5. Exiting loop.")
        break




# sl above last candle if sell
# sl under last candle if buy


# tp = predicted_value