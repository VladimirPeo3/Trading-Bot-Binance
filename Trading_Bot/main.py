from trader import fetch_data, execute_trade, exchange
from strategy import generate_signal, should_take_profit
from risk_manager import calculate_position_size
from utils import log_trade_csv
from indicators import calculate_rsi, calculate_ema
from config import TIMEFRAME, RISK_PERCENT, STOP_LOSS_PERCENT
import pandas as pd
import ccxt

exchange.options['fetchCurrencies'] = False

markets = exchange.load_markets()
SYMBOLS = [s for s in markets if s.endswith('/USDT') and 'DOWN' not in s and 'UP' not in s]

modo_agresivo = False
open_positions = {}

def mostrar_saldo():
    try:
        balance = exchange.fetch_balance()['USDT']['free']
        print(f"\n💰 Saldo disponible: {balance:.2f} USDT")
    except Exception as e:
        print(f"❌ Error al obtener saldo: {e}")

def empezar_trading():
    try:
        balance = exchange.fetch_balance()['USDT']['free']
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

            price = df['close'].iloc[-1]
            signal = generate_signal(df, agresivo=modo_agresivo)
            amount = calculate_position_size(balance, RISK_PERCENT, STOP_LOSS_PERCENT)

            if symbol in open_positions:
                entry = open_positions[symbol]['entry']
                if should_take_profit(entry, price):
                    success = execute_trade(symbol, 'SELL', open_positions[symbol]['amount'])
                    if success:
                        log_trade_csv(symbol, 'SELL', price, open_positions[symbol]['amount'],
                                      df['RSI'].iloc[-1], df['EMA_fast'].iloc[-1], df['EMA_slow'].iloc[-1])
                        print(f"🎯 Venta ejecutada en {symbol} por take profit.")
                        del open_positions[symbol]
                    else:
                        print(f"⚠️ Error al vender {symbol}. Se mantiene la posición.")
                continue

            if signal == 'BUY' and amount >= 2:
                success = execute_trade(symbol, 'BUY', amount)
                if success:
                    open_positions[symbol] = {'entry': price, 'amount': amount}
                    log_trade_csv(symbol, 'BUY', price, amount,
                                  df['RSI'].iloc[-1], df['EMA_fast'].iloc[-1], df['EMA_slow'].iloc[-1])
                    print(f"✅ Compra registrada en {symbol} por ${amount:.2f} a {price}")
            elif signal == 'SELL':
                print("⏸️ No se vende sin posición previa.")
            elif signal in ['BUY', 'SELL']:
                print("⚠️ Señal detectada, pero el monto es menor al mínimo permitido.")
            else:
                print("🕒 Sin señal clara. Esperando próxima oportunidad.")
        except Exception as e:
            print(f"❌ Error al analizar {symbol}: {e}")

def cancelar_posiciones():
    if not open_positions:
        print("📭 No hay posiciones abiertas para cancelar.")
        return

    for symbol in list(open_positions.keys()):
        entry = open_positions[symbol]['entry']
        amount = open_positions[symbol]['amount']
        try:
            current_price = exchange.fetch_ticker(symbol)['last']
            success = execute_trade(symbol, 'SELL', amount)
            if success:
                df = fetch_data(symbol, TIMEFRAME)
                df['EMA_fast'] = calculate_ema(df['close'], 9)
                df['EMA_slow'] = calculate_ema(df['close'], 21)
                df['RSI'] = calculate_rsi(df['close'])

                log_trade_csv(symbol, 'SELL', current_price, amount,
                              df['RSI'].iloc[-1], df['EMA_fast'].iloc[-1], df['EMA_slow'].iloc[-1])
                print(f"🛑 Posición en {symbol} cancelada y vendida a {current_price}")
                del open_positions[symbol]
            else:
                print(f"⚠️ No se pudo vender {symbol}. Se mantiene abierta.")
        except Exception as e:
            print(f"❌ Error al cancelar {symbol}: {e}")

def vender_moneda_manual():
    try:
        balance = exchange.fetch_balance()
        activos = {k: v for k, v in balance['free'].items() if v > 0 and k != 'USDT'}

        if not activos:
            print("📭 No tienes monedas disponibles para vender.")
            return

        print("\n📦 Monedas disponibles para vender:")
        for i, (moneda, cantidad) in enumerate(activos.items(), start=1):
            print(f"{i}. {moneda}: {cantidad}")

        opcion = input("Selecciona el número de la moneda que quieres vender: ")
        try:
            indice = int(opcion) - 1
            moneda = list(activos.keys())[indice]
            cantidad = activos[moneda]
            par = f"{moneda}/USDT"

            ticker = exchange.fetch_ticker(par)
            precio_actual = ticker['last']

            success = execute_trade(par, 'SELL', cantidad)
            if success:
                df = fetch_data(par, TIMEFRAME)
                df['EMA_fast'] = calculate_ema(df['close'], 9)
                df['EMA_slow'] = calculate_ema(df['close'], 21)
                df['RSI'] = calculate_rsi(df['close'])

                log_trade_csv(par, 'SELL', precio_actual, cantidad,
                              df['RSI'].iloc[-1], df['EMA_fast'].iloc[-1], df['EMA_slow'].iloc[-1])
                print(f"✅ Venta manual ejecutada: {cantidad} {moneda} a {precio_actual} USDT")
            else:
                print(f"⚠️ No se pudo vender {moneda}.")
        except Exception as e:
            print(f"❌ Error al procesar la venta: {e}")
    except Exception as e:
        print(f"❌ Error al obtener balances: {e}")

def ver_historial():
    try:
        df = pd.read_csv("trades.csv")
        print("\n📄 Últimas operaciones registradas:")
        print(df.tail(5).to_string(index=False))
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo trades.csv.")
    except Exception as e:
        print(f"❌ Error al leer historial: {e}")

def ver_estadisticas():
    try:
        df = pd.read_csv("trades.csv")

        # Si no tiene encabezado, asignarlo manualmente
        if 'Acción' not in df.columns:
            df.columns = ['Fecha/Hora', 'Par', 'Acción', 'Precio', 'Monto (USDT)', 'RSI', 'EMA rápida', 'EMA lenta', 'Modo']


        total = len(df)
        buy_count = len(df[df['Acción'] == 'BUY'])
        sell_count = len(df[df['Acción'] == 'SELL'])
        avg_rsi = df['RSI'].mean()
        avg_amount = df['Monto (USDT)'].mean()

        print("\n📊 Estadísticas del bot:")
        print(f"Total de operaciones: {total}")
        print(f"BUY: {buy_count} | SELL: {sell_count}")
        print(f"Promedio RSI: {avg_rsi:.2f}")
        print(f"Promedio de monto: ${avg_amount:.2f}")
    except Exception as e:
        print(f"❌ No se pudieron calcular estadísticas: {e}")


def menu():
    global modo_agresivo

    while True:
        print("\n🧠 MENÚ PRINCIPAL")
        print("1. 💰 Ver saldo disponible")
        print("2. 🚀 Empezar trading")
        print("3. 📄 Ver historial de operaciones")
        print("4. 📊 Ver estadísticas del bot")
        print(f"5. 🔁 Modo agresivo: {'Activado' if modo_agresivo else 'Desactivado'}")
        print("6. 🛑 Cancelar todas las posiciones abiertas")
        print("7. 🛒 Vender moneda manualmente")
        print("8. ❌ Salir")

        opcion = input("Selecciona una opción (1-8): ")

        if opcion == '1':
            mostrar_saldo()
        elif opcion == '2':
            empezar_trading()
        elif opcion == '3':
            ver_historial()
        elif opcion == '4':
            ver_estadisticas()
        elif opcion == '5':
            modo_agresivo = not modo_agresivo
            estado = "activado" if modo_agresivo else "desactivado"
            print(f"⚙️ Modo agresivo {estado}.")
        elif opcion == '6':
            cancelar_posiciones()
        elif opcion == '7':
            vender_moneda_manual()
        elif opcion == '8':
            print("👋 Cerrando bot. ¡Hasta la próxima!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
