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

def calculate_rsi(prices, window=14):
    # Calculate RSI
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signals(macd_line, signal_line, rsi):
    # Generate buy/sell signals based on MACD and RSI
    signals = pd.DataFrame(index=macd_line.index)
    signals['Buy'] = np.where((macd_line > signal_line) & (rsi < 30), 1, 0)  # Buy when MACD crosses above signal and RSI is oversold
    signals['Sell'] = np.where((macd_line < signal_line) & (rsi > 70), -1, 0)  # Sell when MACD crosses below signal and RSI is overbought
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_macd_rsi_strategy(prices, macd_line, signal_line, rsi, signals):
    # Plot prices, MACD line, signal line, RSI, and buy/sell signals
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(prices, label='Price')
    plt.plot(macd_line, label='MACD Line', color='blue')
    plt.plot(signal_line, label='Signal Line', color='red')
    plt.title('MACD and Signal Line')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(rsi, label='RSI', color='purple')
    plt.axhline(y=30, color='green', linestyle='--', label='Oversold')
    plt.axhline(y=70, color='orange', linestyle='--', label='Overbought')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()

    plt.figure(figsize=(12, 6))
    plt.plot(prices, label='Price')
    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('MACD and RSI Combined Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'ENGI.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-15'

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate MACD and RSI
    macd_line, signal_line = calculate_macd(prices)
    rsi = calculate_rsi(prices)

    # Generate buy/sell signals
    signals = generate_signals(macd_line, signal_line, rsi)

    # Plot MACD and RSI strategy
    plot_macd_rsi_strategy(prices, macd_line, signal_line, rsi, signals)
