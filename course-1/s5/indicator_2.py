#if the price moves out of the bollinger zone, then there will be a pullback 
# very good return
# import yfinance as yf
# import pandas_ta as ta
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas as pd

# data = yf.download(tickers='BTC-USD', period='max', interval='1d') #data['BB_UPPER'], data['BB_MIDDLE'], data['BB_LOWER'] = 
# data = pd.concat([data, ta.bbands(data.Close, length=14)], axis=1)
# data.columns = data.columns[:6].tolist() + ['BB_LOWER', 'BB_MIDDLE', 'BB_UPPER'] + data.columns[9:].tolist()

# df = data[:500]

# fig = go.Figure()

# fig.add_trace(go.Candlestick(x=df.index,
#                 open=df['Open'],
#                 high=df['High'],
#                 low=df['Low'],
#                 close=df['Close']))
# fig.add_trace(go.Scatter(x=df.index, y=df['BB_UPPER'], name='BB_UPPER'))
# fig.add_trace(go.Scatter(x=df.index, y=df['BB_MIDDLE'], name='BB_MIDDLE'))
# fig.add_trace(go.Scatter(x=df.index, y=df['BB_LOWER'], name='BB_LOWER'))

# fig.update_layout(
#     xaxis=dict(rangeslider=dict(visible=False))
# )

# fig.show()



#atr, is a volatility score, to position the stoploss. if atr is high keep stoploss far & inversely
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

data = yf.download(tickers='BTC-USD', period='max', interval='1d')
data['ATR'] = ta.atr(data.High, data.Low, data.Close, length=14)

df = data[:500]

fig = make_subplots(rows=2, cols=1, subplot_titles=['Price', 'ATR'], shared_xaxes=True)

fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['ATR'], name='ATR'), row=2, col=1)

fig.update_layout(
    xaxis=dict(rangeslider=dict(visible=False))
)

fig.show()