from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Connect to the MetaTrader 5 terminal
mt5.initialize()

symbol = 'GBPUSD'
timeframe = mt5.TIMEFRAME_M5
date_from = datetime(2024, 3, 11)
date_to = datetime.now()
ticks = pd.DataFrame(mt5.copy_rates_range(symbol, timeframe, date_from, date_to))

# Convert the ticks to a Pandas DataFrame
rates = pd.DataFrame(ticks)
rates.columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
rates.set_index('time', inplace=True, drop=False)

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(rates[['open', 'high', 'low', 'close']])

# Create the lagged DataFrame correctly
data_lagged = pd.DataFrame(index=rates.index)
data_lagged['open_lagged'] = pd.Series(scaled_data[:, 0]).shift(1)  # Convert to Series
data_lagged['high_lagged'] = pd.Series(scaled_data[:, 1]).shift(1)
data_lagged['low_lagged'] = pd.Series(scaled_data[:, 2]).shift(1)
data_lagged['close_lagged'] = pd.Series(scaled_data[:, 3]).shift(1)

# Concatenate with scaled data
data_lagged = pd.concat([data_lagged, pd.DataFrame(scaled_data, index=rates.index)], axis=1)

# Build the LSTM model
model = Sequential()
timesteps = 10
model.add(LSTM(50, activation='relu', input_shape=(timesteps, data_lagged.shape[1])))  # shape[1] will be 6
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Train the LSTM model
model.fit(data_lagged, rates['close'], epochs=100, batch_size=32, verbose=0)

# Implement risk management
# Calculate the volatility of the GBP/USD symbol
volatility = np.std(rates['close'])

# Set the risk percentage
risk_percentage = 1

# Implement trading strategy
# Set the stop loss and take profit levels
stop_loss = 20
take_profit = 40

# Set the tick size
tick_size = 0.0001

# Set the account equity
account_equity = 10000

# Calculate the next trading signal
next_signal = model.predict(data_lagged)[0][0]

position_size = int(risk_percentage * account_equity / (stop_loss * volatility))

# Check if the signal is a buy or sell signal
if next_signal > 0:
    # Calculate the entry price
    entry_price = rates['close'][0]
    # Calculate the take profit and stop loss levels
    take_profit_price = entry_price + take_profit * tick_size
    stop_loss_price = entry_price - stop_loss * tick_size
    # Send the trade order to MetaTrader 5
    mt5.order_send(symbol, 0, position_size, entry_price, 0, 0, 0, 0, 0, 0)
else:
    # Calculate the entry price
    entry_price = rates['close'][0]
    # Calculate the take profit and stop loss levels
    take_profit_price = entry_price - take_profit * tick_size
    stop_loss_price = entry_price + stop_loss * tick_size
    # Send the trade order to MetaTrader 5
    mt5.order_send(symbol, 1, abs(position_size), entry_price, 0, 0, 0, 0, 0, 0)

# Shit code
