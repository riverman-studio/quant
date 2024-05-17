import yfinance as yf
from pprint import *
msft = yf.Ticker("RNO.PA")
pprint(msft.get_news())