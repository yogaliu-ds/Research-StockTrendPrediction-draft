
import pandas as pd
import yfinance as yf

from technical_indicator import today_trend, next_day_trend, sma, rsi, kd, macd, tech_final_adjustment

# Setting (Target company)
stock_id = 'MSFT'

# From API, get price history data
df = yf.Ticker(stock_id).history(period='Max')

df = today_trend(df)
df = next_day_trend(df)
df = sma(df)
df = rsi(df)
df = kd(df)
df = macd(df)
df = tech_final_adjustment(df)

# Save to csv, will use in the main.py
df.to_csv('data/processed_technical_indicator.csv', index=False)

# Check the file
x = pd.read_csv('data/processed_technical_indicator.csv')
print(x)
