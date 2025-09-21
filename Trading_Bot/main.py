from config import TIMEFRAME, RISK_PERCENT, STOP_LOSS_PERCENT
from trader import fetch_data, execute_trade, exchange
from strategy import generate_signal
from risk_manager import calculate_position_size
from utils import log_trade
from indicators import calculate_rsi, calculate_ema
import ccxt

# Cargar todos los pares USDT disponibles en Binance
markets = exchange.load_markets()
SYMBOLS = [symbol for symbol in markets if symbol.endswith('/USDT') and 'DOWN' not in symbol and 'UP' not in symbol]

def run_bot():
    try:
        balance = exchange.fetch_balance()['USDT']['free']
        print(f"\n💰 Saldo disponible en USDT: {balance}")
    except Exception as e:
        print(f"❌ Error al obtener saldo: {e}")
        return

    for symbol in SYMBOLS:
        print(f"\n🔍 Analizando {symbol}...")

        try:
            df = fetch_data(symbol, TIMEFRAME)
            df['EMA_fast'] = calculate_ema(df['close'], 9)
            df['EMA_slow'] = calculate_ema(df['close'], 21)
            df['RSI'] = calculate_rsi(df['close'])

            print(df.tail(1)[['EMA_fast', 'EMA_slow', 'RSI', 'volume']])

            signal = generate_signal(df)
            print(f"📡 Señal generada: {signal}")

            if signal == 'BUY':
                print("📈 Cruce alcista + RSI bajo. Señal de compra.")
            elif signal == 'SELL':
                print("📉 Cruce bajista + RSI alto. Señal de venta.")
            else:
                print("⏸️ Mercado neutro o sin confirmación. No se opera.")

            amount = calculate_position_size(balance, RISK_PERCENT, STOP_LOSS_PERCENT)
            price = df['close'].iloc[-1]

            if signal in ['BUY', 'SELL'] and amount >= 10:
                execute_trade(symbol, signal, amount)
                log_trade(signal, price, amount)
            elif signal in ['BUY', 'SELL']:
                print("⚠️ Señal detectada, pero el monto es menor al mínimo permitido.")
            else:
                print("🕒 Esperando próxima oportunidad...")

        except Exception as e:
            print(f"❌ Error al analizar {symbol}: {e}")

if __name__ == "__main__":
    run_bot()
