import asyncio
import json
from typing import Any

import websockets

from storage.state import orderbook


async def stream() -> None:
    url: str = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"

    async with websockets.connect(url) as ws:
        while True:
            msg: str = await ws.recv()
            data: dict[str, Any] = json.loads(msg)

            orderbook["bids"] = data["bids"]
            orderbook["asks"] = data["asks"]


if __name__ == "__main__":
    asyncio.run(stream())