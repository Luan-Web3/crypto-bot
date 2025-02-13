import time
import requests
import hmac
import hashlib
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

from indicators.rsi import RSI

load_dotenv()

SYMBOL = "BTCUSDT"

API_URL = "https://testnet.binance.vision"
# API_URL = "https://api.binance.com"

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

is_opened = False

async def create_order(symbol, side, quantity):
    timestamp = int(time.time() * 1000)
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    
    headers = {"X-MBX-APIKEY": API_KEY}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/api/v3/order", params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
            return None

async def start_bot():
    global is_opened
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=100") as response:
                response.raise_for_status()
                data = await response.json()

        prices = [float(candle[4]) for candle in data]

        rsi = RSI(14).calculate(prices)

        print(f"RSI: {rsi}")

        if rsi < 30 and not is_opened:
            print("Oversold, buying")
            await create_order(SYMBOL, "BUY", 0.0001)
            is_opened = True
        elif rsi > 70 and is_opened:
            print("Overbought, selling")
            await create_order(SYMBOL, "SELL", 0.0001)
            is_opened = False
        else:
            print("Do nothing")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

while True:
    asyncio.run(start_bot())
    time.sleep(3)