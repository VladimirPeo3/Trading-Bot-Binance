# Porcentaje de ganancia objetivo
TAKE_PROFIT_PERCENT = 0.005  # 0.5%

def should_take_profit(entry_price, current_price):
    return current_price >= entry_price * (1 + TAKE_PROFIT_PERCENT)

def generate_signal(df, agresivo=False):
    last = df.iloc[-1]

    if agresivo:
        # Modo agresivo: señales más frecuentes
        if last['EMA_fast'] > last['EMA_slow'] and last['RSI'] < 55:
            return 'BUY'
        elif last['EMA_fast'] < last['EMA_slow'] and last['RSI'] > 45:
            return 'SELL'
    else:
        # Modo conservador: señales más estrictas
        if last['EMA_fast'] > last['EMA_slow'] and last['RSI'] < 30:
            return 'BUY'
        elif last['EMA_fast'] < last['EMA_slow'] and last['RSI'] > 70:
            return 'SELL'

    return None
