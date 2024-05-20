#obv 
# is a buying & selling presure. An increase in volume often preceeds a change in price 
# is a trend confirmation, reversal confirmation & breakout confirmation
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

data = yf.download(tickers='BTC-USD', period='max', interval='1d')
data['OBV'] = ta.obv(data.Close, data.Volume)

df = data[:500]

fig = make_subplots(rows=2, cols=1, subplot_titles=['Price', 'OBV'], shared_xaxes=True)

fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], name='OBV'), row=2, col=1)

fig.update_layout(
    xaxis=dict(rangeslider=dict(visible=False))
)

fig.show()

#CMF:  divergence of price and CMF can signal reversal

import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

data = yf.download(tickers='BTC-USD', period='max', interval='1d')

data['CMF'] = ta.cmf(data.High, data.Low, data.Close, data.Volume, length=20)


df = data[1000:1500]


fig = make_subplots(rows=2, cols=1, subplot_titles=['Price', 'CMF'], shared_xaxes=True)


fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['CMF'], name='CMF'), row=2, col=1)


fig.update_layout(
    xaxis=dict(rangeslider=dict(visible=False))
)


fig.show()