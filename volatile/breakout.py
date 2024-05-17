import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_support_resistance(prices, window):
    # Calculate support and resistance levels based on recent price highs and lows
    support = prices.rolling(window=window, min_periods=1).min()
    resistance = prices.rolling(window=window, min_periods=1).max()
    return support, resistance

def generate_signals(prices, support, resistance):
    # Generate buy/sell signals based on breakout of support/resistance levels
    signals = pd.DataFrame(index=prices.index)
    signals['Buy'] = np.where(prices > resistance.shift(1), 1, 0)  # Buy when price breaks above resistance
    signals['Sell'] = np.where(prices < support.shift(1), -1, 0)  # Sell when price breaks below support
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_breakout_strategy(prices, support, resistance, signals):
    # Plot prices, support/resistance levels, and buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(prices, label='Price')
    plt.plot(support, label='Support', color='green')
    plt.plot(resistance, label='Resistance', color='red')
    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('Breakout Trading Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'ALIMP.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-01'
    window = 20  # Window for calculating support/resistance levels

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate support and resistance levels
    support, resistance = calculate_support_resistance(prices, window)

    # Generate buy/sell signals
    signals = generate_signals(prices, support, resistance)

    # Plot breakout strategy
    plot_breakout_strategy(prices, support, resistance, signals)
