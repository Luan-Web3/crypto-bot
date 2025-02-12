import time
import requests

SYMBOL = "BTCUSDT"
BUY_PRICE = 20000
SELL_PRICE = 20000

API_URL = "https://testnet.binance.vision" # https://api.binance.com

is_opened = False

def start_bot():
    global is_opened
    try:
        response = requests.get(f"{API_URL}/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=21")
        response.raise_for_status()
        data = response.json()
        candle = data[len(data) - 1]
        price = float(candle[4])
        print(f"Price: {price}")
        if price > BUY_PRICE and not is_opened:
            print("Buy")
            is_opened = True
        elif price < SELL_PRICE and is_opened:
            print("Sell")
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