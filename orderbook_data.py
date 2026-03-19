import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

async def stream_orderbook():
    # Stream für die Top 20 Preisstufen von BTC/USDT (Update alle 100ms)
    url = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"
    
    async with websockets.connect(url) as websocket:
        print("Logging gestartet... Drücke STRG+C zum Stoppen.")
        
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            # Zeitstempel hinzufügen
            timestamp = datetime.now()
            
            # Beste Bids und Asks extrahieren (Erstes Element ist der beste Preis)
            best_bid_price = data['bids'][0][0]
            best_bid_qty = data['bids'][0][1]
            best_ask_price = data['asks'][0][0]
            best_ask_qty = data['asks'][0][1]
            
            # Hier würdest du die Daten speichern (z.B. in eine CSV oder DB)
            print(f"[{timestamp}] Bid: {best_bid_price} ({best_bid_qty}) | Ask: {best_ask_price}")

# Das Skript ausführen
try:
    asyncio.run(stream_orderbook())
except KeyboardInterrupt:
    print("Logging beendet.")