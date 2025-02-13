import time
import requests
from indicators.rsi import RSI

SYMBOL = "BTCUSDT"
BUY_PRICE = 20000
SELL_PRICE = 20000

# API_URL = "https://testnet.binance.vision"
API_URL = "https://api.binance.com"

is_opened = False

def start_bot():
    global is_opened
    try:
        response = requests.get(f"{API_URL}/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=100")
        response.raise_for_status()
        data = response.json()

        prices = [float(candle[4]) for candle in data]

        rsi = RSI(14).calculate(prices)

        print(f"RSI: {rsi}")

        if rsi < 30 and not is_opened:
            print("Sobrevendido, comprar")
            is_opened = True
        elif rsi > 70 and is_opened:
            print("Sobrecomprado, vender")
            is_opened = False
        else:
            print("Do nothing")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

while True:
    start_bot()
    time.sleep(3)