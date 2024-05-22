
#####################
#VWAP works on lower time frames, fast movements relatively short time frames
#####################
import yfinance as yf
import pandas_ta as ta
import numpy as np

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

# Download the BTC-USD 15 min data for the last 7 days
data = yf.download('BTC-USD', period='7d', interval='15m')
# Compute the VWAP
data.ta.vwap(append=True)
data['Category'] = check_candles(data, 5, 'VWAP_D') 
data[data["Category"]!=0]

# import plotly.graph_objects as go

# dfpl = data[:]
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])

# # Add the moving averages to the plot
# fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['VWAP_D'], mode='lines', name='VWAP', line=dict(color='red')))

# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()

# Calculate the ADX - to confirm a tred that was detected with the MA or VWAP
data.ta.adx(append=True)
# Define a function to generate the trend signal based on ADX
def generate_trend_signal(data, threshold=40):
    trend_signal = []
    for i in range(len(data)):
        if data['ADX'][i] > threshold:
            if data['DMP'][i] > data['DMN'][i]:
                trend_signal.append(2)  # Confirmed Uptrend
            else:
                trend_signal.append(1)  # Confirmed Downtrend
        else:
            trend_signal.append(0)  # No confirmed trend
    return trend_signal
    # Apply the function to generate the trend signal column
data = data.rename(columns=lambda x: x[:-3] if x.startswith('ADX') else x)
data = data.rename(columns=lambda x: x[:-3] if x.startswith('DM') else x)

data['Trend Signal'] = generate_trend_signal(data)
data[data['Trend Signal']!=0]
# cross chekc with MA/VWAP signal
data['Confirmed Signal'] = data.apply(lambda row: row['Category'] if row['Category'] == row['Trend Signal'] else 0, axis=1)
data[data['Confirmed Signal']!=0]

import plotly.graph_objects as go

dfpl = data[:]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

# Add the moving averages to the plot
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['Confirmed Signal'], mode='lines', name='VWAP', line=dict(color='red')))

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()