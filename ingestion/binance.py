import asyncio
import json
import websockets
from typing import Any

from storage.state import binance_orderbook

async def stream() -> None:
    url: str = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"

    async with websockets.connect(url) as ws:
        while True:
            msg: str = await ws.recv()
            data: dict[str, Any] = json.loads(msg)

            binance_orderbook["bids"] = data["bids"]
            binance_orderbook["asks"] = data["asks"]


if __name__ == "__main__":
    asyncio.run(stream())