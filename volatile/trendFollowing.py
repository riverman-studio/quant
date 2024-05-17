import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_moving_averages(prices, short_window, long_window):
    # Calculate short-term and long-term moving averages
    short_moving_avg = prices.rolling(window=short_window, min_periods=1).mean()
    long_moving_avg = prices.rolling(window=long_window, min_periods=1).mean()
    return short_moving_avg, long_moving_avg

def generate_signals(short_moving_avg, long_moving_avg):
    # Generate buy/sell signals based on moving average crossovers
    signals = pd.DataFrame(index=short_moving_avg.index)
    signals['Buy'] = np.where(short_moving_avg > long_moving_avg, 1, 0)  # Buy when short MA crosses above long MA
    signals['Sell'] = np.where(short_moving_avg < long_moving_avg, -1, 0)  # Sell when short MA crosses below long MA
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_trend_following_strategy(prices, short_moving_avg, long_moving_avg, signals):
    # Plot prices, short-term and long-term moving averages, and buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(prices, label='Price')
    plt.plot(short_moving_avg, label='Short MA', color='red')
    plt.plot(long_moving_avg, label='Long MA', color='green')
    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('Trend-Following Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'CGG.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-15'
    short_window = 20  # Short-term moving average window
    long_window = 50   # Long-term moving average window

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate short-term and long-term moving averages
    short_moving_avg, long_moving_avg = calculate_moving_averages(prices, short_window, long_window)

    # Generate buy/sell signals
    signals = generate_signals(short_moving_avg, long_moving_avg)

    # Plot trend-following strategy
    plot_trend_following_strategy(prices, short_moving_avg, long_moving_avg, signals)
