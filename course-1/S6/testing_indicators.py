import yfinance as yf
import pandas as pd

dataF = yf.download("BTC-USD", start="2022-04-1", end="2023-04-1", interval='1d')
dataF=dataF[dataF["High"]!=dataF['Low']]
dataF.reset_index(inplace=True)
