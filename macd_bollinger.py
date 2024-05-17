import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    # Calculate MACD line and signal line
    short_ema = prices.ewm(span=short_window, min_periods=1).mean()
    long_ema = prices.ewm(span=long_window, min_periods=1).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, min_periods=1).mean()
    return macd_line, signal_line

def calculate_bollinger_bands(prices, window, num_std):
    # Calculate rolling mean and standard deviation
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()

    # Calculate upper and lower Bollinger Bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    return upper_band, lower_band

def generate_signals(macd_line, signal_line, upper_band, lower_band):
    # Generate buy/sell signals based on MACD and Bollinger Bands
    signals = pd.DataFrame(index=macd_line.index)
    signals['Buy'] = np.where((macd_line > signal_line) & (macd_line < upper_band), 1, 0)  # Buy when MACD is below upper band
    signals['Sell'] = np.where((macd_line < signal_line) & (macd_line > lower_band), -1, 0)  # Sell when MACD is above lower band
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_macd_bollinger_strategy(prices, macd_line, signal_line, upper_band, lower_band, signals):
    # Plot prices, MACD line, signal line, Bollinger Bands, and buy/sell signals
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(prices, label='Price')
    plt.plot(macd_line, label='MACD Line', color='blue')
    plt.plot(signal_line, label='Signal Line', color='red')
    plt.title('MACD and Signal Line')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(prices, label='Price')
    plt.plot(upper_band, label='Upper Bollinger Band', color='red')
    plt.plot(lower_band, label='Lower Bollinger Band', color='green')
    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('Bollinger Bands Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'CGG.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-15'
    short_window = 12  # MACD short-term window
    long_window = 26   # MACD long-term window
    signal_window = 9  # MACD signal window
    bollinger_window = 20  # Bollinger Bands window
    num_std = 2  # Number of standard deviations for Bollinger Bands

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate MACD
    macd_line, signal_line = calculate_macd(prices, short_window, long_window, signal_window)

    # Calculate Bollinger Bands
    upper_band, lower_band = calculate_bollinger_bands(prices, bollinger_window, num_std)

    # Generate buy/sell signals
    signals = generate_signals(macd_line, signal_line, upper_band, lower_band)

    # Plot MACD and Bollinger Bands strategy
    plot_macd_bollinger_strategy(prices, macd_line, signal_line, upper_band, lower_band, signals)
