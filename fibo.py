import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_fibonacci_retracement(prices, high, low):
    # Calculate Fibonacci retracement levels
    fibonacci_levels = [0, 0.236, 0.382, 0.5, 0.618, 1]
    fibonacci_prices = {}

    for level in fibonacci_levels:
        fibonacci_prices[level] = high - (high - low) * level

    return fibonacci_prices

def generate_signals(prices, fibonacci_prices):
    # Generate buy/sell signals based on Fibonacci retracement levels
    signals = pd.DataFrame(index=prices.index)
    signals['Buy'] = np.where(prices <= fibonacci_prices[0.382], 1, 0)  # Buy at 38.2% retracement level
    signals['Sell'] = np.where(prices >= fibonacci_prices[0.618], -1, 0)  # Sell at 61.8% retracement level
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_fibonacci_retracement(prices, fibonacci_prices, signals):
    # Plot prices, Fibonacci retracement levels, and buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(prices, label='Price')

    for level, price in fibonacci_prices.items():
        plt.axhline(y=price, color='red', linestyle='--', label=f'Fib {level}')

    plt.plot(signals.loc[signals['Signal'] == 1].index, prices[signals['Signal'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(signals.loc[signals['Signal'] == -1].index, prices[signals['Signal'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

    plt.title('Fibonacci Retracement Strategy with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    symbol = 'AI.PA'
    start_date = '2021-09-01'
    end_date = '2023-01-09'

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate Fibonacci retracement levels
    high = prices.max()
    low = prices.min()
    fibonacci_prices = calculate_fibonacci_retracement(prices, high, low)

    # Generate buy/sell signals
    signals = generate_signals(prices, fibonacci_prices)

    # Plot Fibonacci retracement levels with buy/sell signals
    plot_fibonacci_retracement(prices, fibonacci_prices, signals)
