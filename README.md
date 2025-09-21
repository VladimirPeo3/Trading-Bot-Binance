# 🤖 Trading Bot Binance

Bot de trading automatizado para criptomonedas en Binance, diseñado para operar pares USDT utilizando señales técnicas como RSI y EMAs. Incluye un menú interactivo, control de riesgo, seguimiento de posiciones, y opciones manuales para una experiencia flexible y robusta.

---

## 🚀 Funcionalidades

### 🧠 Menú interactivo
Controla el bot desde consola con opciones como:

- `1. Ver saldo disponible`  
- `2. Empezar trading`  
- `3. Ver historial de operaciones`  
- `4. Ver estadísticas del bot`  
- `5. Activar/desactivar modo agresivo`  
- `6. Cancelar posiciones abiertas`  
- `7. Vender moneda manualmente`  
- `8. Salir`

### 📊 Estrategia técnica
- Señales basadas en RSI y cruce de EMAs
- Modo agresivo para señales más frecuentes
- Modo conservador para filtros estrictos

### 💼 Gestión de riesgo
- Cálculo automático del tamaño de posición
- Configuración de `RISK_PERCENT` y `STOP_LOSS_PERCENT`
- Evita operaciones si el monto es menor al mínimo permitido

### 🎯 Take Profit automático
- Seguimiento de posiciones abiertas
- Venta automática si el precio supera el objetivo de ganancia

### 🛑 Cancelación manual
- Cierra todas las posiciones abiertas desde el menú

### 🛒 Venta manual de activos
- Muestra monedas con saldo disponible
- Permite vender cualquier activo desde tu cuenta Binance

### 📄 Historial y estadísticas
- Registro en `trades.csv` con RSI, EMAs, monto y acción
- Estadísticas agregadas: total de operaciones, promedio RSI, monto medio, distribución BUY/SELL

---

## 🔐 Configuración de claves API Binance

Para que el bot se conecte a tu cuenta de Binance, necesitas una API Key y Secret. Puedes generarlas desde [Binance API Management](https://www.binance.com/es/my/settings/api-management) y luego configurarlas en tu archivo `trader.py`:

```python
import ccxt

exchange = ccxt.binance({
    'apiKey': 'TU_API_KEY',
    'secret': 'TU_API_SECRET',
    'enableRateLimit': True
})
