import csv
from datetime import datetime

def log_trade_csv(symbol, action, price, amount, rsi, ema_fast, ema_slow):
    with open('trades.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symbol, action, round(price, 4), round(amount, 2),
            round(rsi, 2), round(ema_fast, 4), round(ema_slow, 4)
        ])
