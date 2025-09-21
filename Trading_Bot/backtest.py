from strategy import generate_signal

def backtest(df):
    signals = []
    for i in range(21, len(df)):
        sub_df = df.iloc[i-21:i]
        signal = generate_signal(sub_df)
        signals.append((df['timestamp'].iloc[i], signal))
    return signals
