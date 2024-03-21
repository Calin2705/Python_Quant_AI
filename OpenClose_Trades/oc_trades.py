import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import time
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

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

def open_trade(symbol, action, volume):
    request = {
        "action": action,             # Trade action: mt5.ORDER_BUY or mt5.ORDER_SELL
        "symbol": symbol,             # Symbol to trade
        "volume": volume,             # Trade volume
        "type": mt5.ORDER_TYPE_MARKET,# Order type
        "type_filling": mt5.ORDER_FILLING_RETURN,  # Order filling type
    }

    result = mt5.order_send(request)
    return result

while True:
    if mt5.initialize():
        symbol = 'GBPUSD'
        timeframe = mt5.TIMEFRAME_M1
        date_from = datetime(2024, 3, 11)
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

        model.fit(X, y, epochs=100, batch_size=32)

        last_sequence = target_scaled[-sequence_length:].reshape(1, sequence_length, 1)
        predicted_value = model.predict(last_sequence)
        predicted_value = scaler.inverse_transform(predicted_value)[0][0]

        last_close = data['close'].iloc[-1]

        print("Predicted value:", predicted_value)
        print("Last close value:", last_close)
        print(data[-2:])

        # Compare last close with predicted value
        if last_close > predicted_value:
            print("Last close is greater than predicted value.")
            # Open a sell trade
            result = open_trade(symbol, mt5.ORDER_SELL, 0.1)  # Adjust volume as needed
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Failed to open sell trade:", result.comment)
        elif last_close < predicted_value:
            print("Last close is less than predicted value.")
            # Open a buy trade
            result = open_trade(symbol, mt5.ORDER_BUY, 0.1)  # Adjust volume as needed
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Failed to open buy trade:", result.comment)
        else:
            print("Last close is equal to predicted value.")

        time.sleep(60)
    else:
        print("Failed to initialize MetaTrader 5. Exiting loop.")
        break
