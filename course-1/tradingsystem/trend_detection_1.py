# MOVING AVERAGE DETECTTION

import yfinance as yf
import pandas_ta as ta
import numpy as np

def get_data(symbol: str):
    data = yf.download(tickers=symbol, period='100d', interval='1d')
    data.reset_index(inplace=True, drop=True)
    return data
# Get the data
data = get_data('BTC-USD')


def calculate_sma(data, length: int):
    return ta.sma(data['Close'], length)

# Calculate the moving average
data['SMA'] = calculate_sma(data, 20)
data.dropna(inplace=True)

#calculate average + or - over a period of 5 candles
def calculate_slope(series, period: int = 5):
    slopes = [0 for _ in range(period-1)]
    for i in range(period-1, len(series)):
        x = np.arange(period)
        y = series[i-period+1:i+1].values
        slope = np.polyfit(x, y, 1)[0]  # Calculate the slope using linear regression
        percent_slope = (slope / y[0]) * 100  # Convert the slope to a percentage
        slopes.append(percent_slope)
    return slopes


data['Slope'] = calculate_slope(data['SMA'])
data.reset_index(inplace=True, drop=True)

# import plotly.graph_objects as go

# dfpl = data[:]
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])

# fig.add_scatter(x=dfpl.index, y=dfpl['SMA'], mode="markers",
#                 marker=dict(size=5, color="MediumPurple"),
#                 name="pivot")
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()


# Calculate the moving averages STRATEGY 2
data['SMA_10'] = calculate_sma(data, 10)
data['SMA_20'] = calculate_sma(data, 20)
data['SMA_30'] = calculate_sma(data, 30)

def determine_trend(data):
    if data['SMA_10'] > data['SMA_20'] > data['SMA_30']:
        return 2  # Uptrend
    elif data['SMA_10'] < data['SMA_20'] < data['SMA_30']:
        return 1  # Downtrend
    else:
        return 0  # No trend

# Determine the trend and add it as a new column to the DataFrame
data['Trend'] = data.apply(determine_trend, axis=1)


import plotly.graph_objects as go

# dfpl = data[:]
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])

# # Add the moving averages to the plot
# fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_10'], mode='lines', name='SMA 10', line=dict(color='blue')))
# fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_20'], mode='lines', name='SMA 20', line=dict(color='red')))
# fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_30'], mode='lines', name='SMA 30', line=dict(color='green')))

# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()
## 3 - Candles above or below the MA curve 6 STRATEGY 3
def check_candles(data, backcandles, ma_column):
    categories = [0 for _ in range(backcandles)]
    for i in range(backcandles, len(data)):
        if all(data['Close'][i-backcandles:i] > data[ma_column][i-backcandles:i]):
            categories.append(2)  # Uptrend
        elif all(data['Close'][i-backcandles:i] < data[ma_column][i-backcandles:i]):
            categories.append(1)  # Downtrend
        else:
            categories.append(0)  # No trend
    return categories

# Apply the function to the DataFrame
data['Category'] = check_candles(data, 5, 'SMA_20')

import plotly.graph_objects as go

dfpl = data[:]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

# Add the moving averages to the plot
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_20'], mode='lines', name='SMA 20', line=dict(color='red')))

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()

