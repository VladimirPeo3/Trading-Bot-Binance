import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
df = pd.read_csv("trades.csv", header=None)
df.columns = ['Fecha/Hora', 'Par', 'Acción', 'Precio', 'Monto (USDT)', 'RSI', 'EMA rápida', 'EMA lenta']


# Estadísticas clave
total = len(df)
buy_count = len(df[df['Acción'] == 'BUY'])
sell_count = len(df[df['Acción'] == 'SELL'])
avg_rsi_buy = df[df['Acción'] == 'BUY']['RSI'].mean()
avg_rsi_sell = df[df['Acción'] == 'SELL']['RSI'].mean()
avg_amount = df['Monto (USDT)'].mean()
most_traded = df['Par'].value_counts().idxmax()
avg_price_buy = df[df['Acción'] == 'BUY']['Precio'].mean()
avg_price_sell = df[df['Acción'] == 'SELL']['Precio'].mean()

# Mostrar resumen
print("\n📊 Resumen de operaciones registradas:")
print(f"Total de operaciones: {total}")
print(f"BUY: {buy_count} | SELL: {sell_count}")
print(f"Promedio RSI BUY: {avg_rsi_buy:.2f}")
print(f"Promedio RSI SELL: {avg_rsi_sell:.2f}")
print(f"Promedio de monto invertido: ${avg_amount:.2f}")
print(f"Par más operado: {most_traded}")
print(f"Precio promedio BUY: {avg_price_buy:.4f}")
print(f"Precio promedio SELL: {avg_price_sell:.4f}")

# 📈 Gráfico RSI por operación
plt.figure(figsize=(10, 6))
plt.plot(df['Fecha/Hora'], df['RSI'], marker='o', linestyle='-', color='blue', label='RSI')
plt.axhline(70, color='red', linestyle='--', label='Sobrecompra (70)')
plt.axhline(30, color='green', linestyle='--', label='Sobreventa (30)')
plt.xticks(rotation=45)
plt.title('RSI por operación registrada')
plt.xlabel('Fecha/Hora')
plt.ylabel('RSI')
plt.legend()
plt.tight_layout()
plt.show()
