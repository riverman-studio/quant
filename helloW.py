import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Function to fetch historical price data using Yahoo Finance API
def get_price_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Adj Close']

# Function to fit ARIMA model and predict future price
def predict_future_price(symbol, start_date, end_date, order, future_date):
    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)
    
    # Fit ARIMA model
    model = ARIMA(prices, order=order)
    model_fit = model.fit()

    # Predict future price
    future_price = model_fit.forecast(steps=(future_date - prices.index[-1]).days)[0]
    return future_price

if __name__ == "__main__":
    symbol = 'RNO.PA'
    start_date = '2023-09-01'
    end_date = '2024-05-09'
    order = (5, 1, 0)  # Example ARIMA order
    future_date = '2024-05-13'

    future_price = predict_future_price(symbol, start_date, end_date, order, pd.to_datetime(future_date))
    print(f"Predicted price for {future_date}: ${future_price:.2f}")





def main():
    # Input parameters
    symbol = "RNO.PA"
    start_date = "2023-09-01"
    end_date = "2024-05-01"
    n_components = 5

    # Fetch historical price data
    prices = get_price_data(symbol, start_date, end_date)

    # Fit HMM model
    model = fit_hmm_model(prices, n_components)

    # Plot HMM model predictions
    plot_hmm_model(prices, model)

if __name__ == "__main__":
    main()
