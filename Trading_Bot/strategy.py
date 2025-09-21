from indicators import calculate_rsi, calculate_ema

def generate_signal(df):
    df['EMA_fast'] = calculate_ema(df['close'], 9)
    df['EMA_slow'] = calculate_ema(df['close'], 21)
    df['RSI'] = calculate_rsi(df['close'])

    last = df.iloc[-1]

    if last['EMA_fast'] > last['EMA_slow'] and last['RSI'] < 30:
        return 'BUY'
    elif last['EMA_fast'] < last['EMA_slow'] and last['RSI'] > 70:
        return 'SELL'
    else:
        return 'WAIT'
