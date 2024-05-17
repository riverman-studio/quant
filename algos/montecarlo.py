import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_price_data(symbol, start_date, end_date):
    # Function to fetch historical price data using Yahoo Finance API
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

def monte_carlo_simulation(prices, num_simulations, num_days):
    returns = prices.pct_change()
    mean_daily_return = returns.mean()
    std_daily_return = returns.std()

    simulations = np.zeros((num_days, num_simulations))

    for i in range(num_simulations):
        daily_returns = np.random.normal(mean_daily_return, std_daily_return, num_days)
        price_series = np.zeros(num_days)
        price_series[0] = prices.iloc[-1]

        for j in range(1, num_days):
            price_series[j] = price_series[j-1] * (1 + daily_returns[j])

        simulations[:, i] = price_series

    return simulations

def generate_signals(prices, simulations, buy_threshold=75, sell_threshold=25):
    buy_signal = np.percentile(simulations[-1], buy_threshold)
    sell_signal = np.percentile(simulations[-1], sell_threshold)
    signals = pd.DataFrame(index=prices.index)
    signals['Buy'] = np.where(prices > buy_signal, 1, 0)
    signals['Sell'] = np.where(prices < sell_signal, -1, 0)
    signals['Signal'] = signals['Buy'] + signals['Sell']
    return signals

def plot_monte_carlo_simulation(prices, simulations, signals):
    plt.figure(figsize=(12, 6))
    plt.plot(prices.index, prices, label='Actual Price', color='blue')
    
    new_dates = pd.date_range(start=prices.index[-1] + pd.Timedelta(days=1), periods=simulations.shape[0])
    plt.plot(new_dates, np.mean(simulations, axis=1), label='Mean Simulation', color='orange')
    
    buy_dates = signals.index[signals['Signal'] == 1]
    buy_prices = prices.loc[buy_dates]
    plt.scatter(buy_dates, buy_prices, color='green', marker='^', label='Buy Signal')
    
    sell_dates = signals.index[signals['Signal'] == -1]
    sell_prices = prices.loc[sell_dates]
    plt.scatter(sell_dates, sell_prices, color='red', marker='v', label='Sell Signal')
    
    plt.title('Monte Carlo Simulation of Stock Prices with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()



if __name__ == "__main__":
    symbol = 'ENGI.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-15'
    num_simulations = 100
    num_days = 252  # Number of trading days in a year
    buy_threshold = 75  # Percentile for buy signal
    sell_threshold = 25  # Percentile for sell signal

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Perform Monte Carlo simulation
    simulations = monte_carlo_simulation(prices, num_simulations, num_days)

    # Generate buy/sell signals
    signals = generate_signals(prices, simulations, buy_threshold, sell_threshold)

    # Plot Monte Carlo simulation with buy/sell signals
    plot_monte_carlo_simulation(prices, simulations, signals)
