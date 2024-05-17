import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Function to fetch historical price data using Yahoo Finance API
def get_price_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close'].values.reshape(-1, 1)

# Function to prepare the data for LSTM model
def prepare_data(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps - 1):
        X.append(data[i:(i+n_steps), 0])
        y.append(data[i + n_steps, 0])
    return np.array(X), np.array(y)

# Fetch historical price data
symbol = 'RNO.PA'
start_date = '2022-01-01'
end_date = '2024-01-01'
price_data = get_price_data(symbol, start_date, end_date)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(price_data)

# Define the number of time steps for LSTM
n_steps = 60

# Prepare the data for LSTM model
X, y = prepare_data(scaled_data, n_steps)

# Reshape data for LSTM input: [samples, time steps, features]
X = X.reshape((X.shape[0], X.shape[1], 1))

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(n_steps, 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=10, batch_size=32)

# Make predictions
future_days = 30
future_dates = pd.date_range(start=end_date, periods=future_days + 1)[1:]
future_prices = []

# Use the last n_steps data points from the original data as input for prediction
input_data = scaled_data[-n_steps:].reshape((1, n_steps, 1))

for i in range(future_days):
    predicted_price = model.predict(input_data)[0, 0]
    future_prices.append(predicted_price)
    input_data = np.append(input_data[:, 1:, :], [[[predicted_price]]], axis=1)

# Inverse transform the predicted prices to get the actual price values
predicted_prices = scaler.inverse_transform(np.array(future_prices).reshape(-1, 1))

# Create a DataFrame to store the predicted prices with dates
predicted_df = pd.DataFrame(predicted_prices, index=future_dates, columns=['Predicted Price'])

# Plot actual and predicted prices
plt.figure(figsize=(12, 6))
plt.plot(price_data, label='Actual Price', color='blue')
plt.plot(predicted_df.index, predicted_df['Predicted Price'], label='Predicted Price', color='orange')
plt.title('Actual vs Predicted Stock Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
