import pandas as pd
import numpy as np


# (1) Today Trend
def today_trend(df):
    # Get numerical
    df['Today_trend'] = df['Close'] - df['Open']

    # Get categorical

    # Positive = 2
    # neutral = 1
    # Negative = 0

    # Let's try no neutral
    temp_list = []
    for i in df['Today_trend']:
        # if i == 0:
        #   temp_list.append(1)
        if i >= 0:
            temp_list.append(1)
        else:
            temp_list.append(0)

    # Append to df
    df['Today_trend_cate'] = temp_list

    # Change datatype to 'category'
    df['Today_trend_cate'] = df['Today_trend_cate'].astype('category')

    return df


# (2) Next Day Trend
def next_day_trend(df):
    # Get numerical
    temp_close = df['Close']

    temp_list = []

    x = -1
    y = 0
    while True:
        x += 1
        y += 1
        temp_value = temp_close[y] - temp_close[x]
        temp_list.append(temp_value)

        # Transform index, should be subtracted by 1
        if y == (df.shape[0] - 1):
            break

    # append a useless value to the end. To make sure the sample size is same
    temp_list.append(0)
    df['Tomorrow_trend'] = temp_list

    # Get categorical

    # Positive = 2
    # neutral = 1
    # Negative = 0

    temp_list = []
    for i in df['Tomorrow_trend']:
        # if i == 0:
        #   temp_list.append(1)
        if i >= 0:
            temp_list.append(1)
        else:
            temp_list.append(0)

    # Append to df
    df['Tomorrow_trend_cate'] = temp_list

    # Change datatype to 'category'
    df['Tomorrow_trend_cate'] = df['Tomorrow_trend_cate'].astype('category')

    return df


# (3) SMA (Simple Moving Average)
def sma(df):
    # 1. The average of past 14 days
    temp_close = df['Close']
    temp_list = []
    x = -1
    while True:
        x += 1
        first_few_sma = temp_close[x:x + 14].mean()
        temp_list.append(first_few_sma)

        # Transform to index, should be subtracted by 1
        if x + 13 == (df.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    for i in range(13):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_sma = temp_zeros + temp_list

    # 4. Combine into one df
    df['Sma'] = temp_sma

    return df


# (4) RSI (Relative Strength Indicator)
def rsi(df):
    # 1.
    temp_high = df['High']
    temp_low = df['Low']

    temp_list = []
    x = -1
    while True:
        x += 1
        n = 14
        high = temp_high[x:x + n].max()
        low = temp_low[x:x + n].min()

        # formula
        one_rsi = 100 - (100 / (1 + (high / low)))
        temp_list.append(one_rsi)

        # Transform to index, should be subtracted by 1
        if x + (n - 1) == (df.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    for i in range(13):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_rsi = temp_zeros + temp_list

    # 4. Combine into one df
    df['Rsi'] = temp_rsi

    return df


# (5) KD (Stochastic Oscillator)
def kd(df):
    # 1.
    temp_high = df['High']
    temp_low = df['Low']
    temp_close = df['Close']

    temp_list = []
    x = -1
    n = 14
    while True:
        x += 1

        high = temp_high[x:x + n].max()
        low = temp_low[x:x + n].min()
        close = temp_close[x + n - 1]

        # formula
        one_kd = (close - low) / (high - low) * 100
        temp_list.append(one_kd)

        # Transform to index, should be subtracted by 1
        if x + (n - 1) == (df.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    # n = 14 here
    for i in range(n - 1):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_kd = temp_zeros + temp_list

    # 4. Combine into one df
    df['Kd'] = temp_kd

    return df


# (6) MACD (Moving Average Convergence/ Divergence)
def macd(df):
    # EMA 12 Days
    # 1. EMA(12 days)
    temp_close = df['Close']

    # Calculate the first EMA
    x = 0
    n = 12
    ema_second_day = temp_close[x:x + n].mean()
    temp_list = [ema_second_day]

    # Here we calculate the first one by ourselves, so we should add x by 1
    x = 0
    n = 12
    smoothing = 2 / (1 + n)

    ema_yesterday = ema_second_day
    while True:
        x += 1

        close = temp_close[x + n - 1]

        # formula
        ema = close * (smoothing / (1 + n)) + ema_yesterday * (1 - (smoothing / (1 + n)))
        # Save for next loop
        ema_yesterday = ema
        # append to the list
        temp_list.append(ema)

        # Transform to index, should be subtracted by 1
        # Final_index = df.shape[0]-1
        if x + (n - 1) == (df.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    # n = 12 here
    for i in range(n - 1):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_ema_12 = temp_zeros + temp_list

    df['Ema_12'] = temp_ema_12


    # EMA 26 days
    # 1. EMA(26 days)
    temp_close = df['Close']

    # Calculate the first EMA
    x = 0
    n = 26
    ema_second_day = temp_close[x:x + n].mean()
    temp_list = [ema_second_day]

    # Here we calculate the first one by ourselves, so we should add x by 1
    x = 0
    n = 26
    smoothing = 2 / (1 + n)

    ema_yesterday = ema_second_day
    while True:
        x += 1

        close = temp_close[x + n - 1]

        # formula
        ema = close * (smoothing / (1 + n)) + ema_yesterday * (1 - (smoothing / (1 + n)))
        ema_yesterday = ema
        temp_list.append(ema)

        # Transform to index, should be subtracted by 1
        # Final_index = df.shape[0]-1
        if x + (n - 1) == (df.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []

    # n = 26 here
    for i in range(n - 1):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_ema_26 = temp_zeros + temp_list

    df['Ema_26'] = temp_ema_26

    # MACD = EMA(12) - EMA(26)
    df['Macd'] = df['Ema_12'] - df['Ema_26']
    return df


# 3. Final adjustment
def tech_final_adjustment(df):
    # (1) Drop useless columns
    # (2) Move index to column "datetime"
    # move the index to column "datetime"
    df['datetime'] = df.index
    # remove the time zone information
    x = pd.to_numeric(df['datetime'])
    x = pd.to_datetime(x)
    df['datetime'] = x

    # Remove time information, only contains date
    temp_list = []
    for i in df['datetime']:
        i = i.date()

        # Surprising that it can be changed like this
        i = np.datetime64(i)
        temp_list.append(i)

    df['datetime'] = temp_list

    return df

# ----------
# (3) Save to csv
# Save csv
# df.to_csv('/content/drive/MyDrive/Research/tech_indicator/tech_indicator.csv', index=False)
