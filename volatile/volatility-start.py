import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def calculate_bollinger_bands(prices, window, num_std):
    # Calculate rolling mean and standard deviation
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()

    # Calculate upper and lower Bollinger Bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    return upper_band, lower_band

def generate_signals(prices, upper_band, lower_band):
    # Generate buy/sell signals based on Bollinger Bands
    signals = pd.DataFrame(index=prices.index)
    signals['Buy'] = np.where(prices < lower_band, 1, 0)  # Buy when price falls below lower band
    signals['Sell'] = np.where(prices > upper_band, -1, 0)  # Sell when price rises above upper band
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_bollinger_bands(prices, upper_band, lower_band, signals):
    # Plot prices, Bollinger Bands, and buy/sell signals
    plt.figure(figsize=(12, 6))
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
    end_date = '2024-05-01'
    window = 20  # Bollinger Bands window (number of periods)
    num_std = 2  # Number of standard deviations for upper/lower bands

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Calculate Bollinger Bands
    upper_band, lower_band = calculate_bollinger_bands(prices, window, num_std)

    # Generate buy/sell signals
    signals = generate_signals(prices, upper_band, lower_band)

    # Plot Bollinger Bands and signals
    plot_bollinger_bands(prices, upper_band, lower_band, signals)
