import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_macd(prices, short_window, long_window, signal_window):
    # Calculate short-term and long-term exponential moving averages
    short_ema = prices.ewm(span=short_window, min_periods=1).mean()
    long_ema = prices.ewm(span=long_window, min_periods=1).mean()

    # Calculate MACD line
    macd_line = short_ema - long_ema

    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_window, min_periods=1).mean()

    return macd_line, signal_line

def generate_signals(macd_line, signal_line):
    # Generate buy/sell signals based on MACD line and signal line crossovers
    signals = pd.DataFrame(index=macd_line.index)
    signals['Buy'] = np.where(macd_line > signal_line, 1, 0)
    signals['Sell'] = np.where(macd_line < signal_line, -1, 0)
    signals['Signal'] = signals['Buy'] + signals['Sell']

    return signals

def plot_macd(prices, macd_line, signal_line, signals):
    # Plot MACD line, signal line, and buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(prices, label='Price')
    # plt.plot(macd_line, label='MACD Line', color='red')
    # plt.plot(signal_line, label='Signal Line', color='green')
    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('MACD Indicator')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'ENGI.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-15'
    short_window = 12  # Short-term EMA window
    long_window = 26  # Long-term EMA window
    signal_window = 9  # Signal line window

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate MACD line and signal line
    macd_line, signal_line = calculate_macd(prices, short_window, long_window, signal_window)

    # Generate buy/sell signals
    signals = generate_signals(macd_line, signal_line)

    # Plot MACD line, signal line, and signals
    plot_macd(prices, macd_line, signal_line, signals)
