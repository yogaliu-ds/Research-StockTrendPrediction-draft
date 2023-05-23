# 1. Price History



# 1. import
# Basic
import pandas as pd
import numpy as np

# Others
import yfinance as yf
from datetime import datetime, timedelta
import statistics


# Specify the target company
stock_id = 'MSFT'
news_data_location = 'data/microsoft_article_business.csv'

# 1. Technical Indicators
# 1.1 API, get the data
df = yf.Ticker(stock_id).history(period='Max')

# only get part of the samples
# df = df.iloc[:5000]

# Check it out
print(df.shape)
print(df.head())
print(df.tail())
