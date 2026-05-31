import asyncio
import json
import websockets

async def stream():
    url = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"

    orderbook = {
        "bids": [],
        "asks": []
    }

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            orderbook["bids"] = data["bids"]
            orderbook["asks"] = data["asks"]

            best_bid = float(orderbook["bids"][0][0])
            best_ask = float(orderbook["asks"][0][0])

            spread = best_ask - best_bid

            print(
                f"Bid: {best_bid} | "
                f"Ask: {best_ask} | "
                f"Spread: {spread}"
            )

asyncio.run(stream())