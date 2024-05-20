import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
df = pd.read_csv("course-1/BTCUSD_Candlestick_1_D_ASK_08.05.2017-16.10.2021.csv")
# df["EMA"] = ta.ema(df.Close, length=10)
# df["RSI_10"] = ta.rsi(df.Close, length=10)
# dpfl = df[0:50]
# fig = go.Figure(data = [go.Candlestick(x=dpfl.index, open=dpfl["Open"], high = dpfl["High"], low=dpfl["Low"], close = dpfl["Close"]), 
#                         go.Scatter(x=dpfl.index, y=dpfl.EMA, line= dict(color='red', width=2), name="EMA"),
#                         go.Scatter(x=dpfl.index, y=dpfl.RSI_10, line= dict(color='blue', width=2), name="RSI_10")])
# fig.show()

df.ta.indicators()
# /help(ta.rsi)   <<< very helpful

import matplotlib.pyplot as plt
plt.plot(df.index, df.Close)
plt.show()