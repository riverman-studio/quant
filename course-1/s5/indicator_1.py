import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
data = yf.download(tickers="BTC-USD", period="max", interval="1d")
from plotly.subplots import make_subplots
df = data[:500]

# ta.adx(...) is a trend indicator that can lead traders to reduced risk and increase profit potential
# ideal must be between 40 to 60, anything abouve 60 is volatility / noise
#df["ADX"] = ta.adx(df['High'], df['Low'], df['Close'], length = 14)['ADX_14']  


# ta.rsi(...) is oversold (-30) / overbaught (+70) indicator: 
# 50-70 bullish +ive trend
# 30-50 moderate bullish +ive trend
# 50-30 strong bearish -ive trend
# 70-50 moderate bullish -ive trend
# depends on the direction 

data["RSI_10"] = ta.rsi(data.Close, length=10)
df = data[:500]

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='OHLC'),
                go.Scatter(x=df.index, y=df['RSI_10'], name='RSI', yaxis='y2')
                ])

fig.update_layout(
    title='OHLC with RSI(10)',
    yaxis=dict(
        domain=[0.2, 1]
    ),
    yaxis2=dict(
        domain=[0, 0.2],
        anchor='free',
        overlaying='y',
        side='right',
        title='RSI'
    ))

fig.show()


#  ta.stoch(...)

# Create a subplot, and position is 1 row x 2 columns
df.ta.stoch(high='High', low='Low', close='Close', fast_k=14, slow_k=3, slow_d=3, append=True)
fig = make_subplots(rows=2, cols=1)

# In the first row, plot the candlestick chart
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)

# In the second row, plot the ADX
fig.add_trace(go.Scatter(x=df.index, y=df['STOCHk_14_3_3'], name='S1'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['STOCHd_14_3_3'], name='S2'), row=2, col=1)
fig.update_layout(
    xaxis=dict(rangeslider=dict(visible=False)),
    xaxis2=dict(rangeslider=dict(visible=False))
)

fig.show()