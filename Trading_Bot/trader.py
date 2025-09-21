import ccxt
import pandas as pd
from config import API_KEY, API_SECRET

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True
})

def execute_trade(symbol, side, amount):
    try:
        if side == 'BUY':
            exchange.create_market_buy_order(symbol, amount)
        elif side == 'SELL':
            exchange.create_market_sell_order(symbol, amount)
        print(f"✅ Orden {side} ejecutada en {symbol} con {amount} USDT")
    except Exception as e:
        print(f"❌ Error al ejecutar orden en {symbol}: {e}")

def fetch_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df
